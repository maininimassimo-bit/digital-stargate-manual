package it.digitalstargate.allskypocket

import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.time.Instant
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.time.format.ResolverStyle

internal const val ORIGIN = "https://digitalstargate.freeddns.it:23232"
internal const val POLL_INTERVAL_MS = 30_000L
internal fun isProjectionFresh(generated: Instant?, now: Instant): Boolean =
    generated != null && !generated.isAfter(now.plusSeconds(30)) && !generated.isBefore(now.minusSeconds(150))
internal fun isCameraFresh(shotAt: Instant?, now: Instant): Boolean =
    shotAt != null && !shotAt.isAfter(now.plusSeconds(30)) && !shotAt.isBefore(now.minusSeconds(180))
private const val CONNECT_TIMEOUT_MS = 8_000
private const val READ_TIMEOUT_MS = 12_000
private const val MAX_RESPONSE_BYTES = 2_000_000

internal data class WeatherSnapshot(
    val generatedAt: Instant?, val observedAt: Instant?, val freshUntil: Instant?,
    val temperatureC: Double?, val humidityPct: Double?, val dewPointC: Double?, val windKmh: Double?,
    val fresh: Boolean,
)

internal data class ArchiveItem(val date: String, val file: String, val category: String, val mediaType: String)
internal data class MeteorCandidate(val file: String, val timestamp: Instant)

internal data class ProjectionSnapshot(val generatedAt: Instant?, val weather: WeatherSnapshot, val camera: CameraSnapshot)
internal data class CameraSnapshot(val fileName: String?, val shotAt: Instant?)

object AllskyRepository {
    internal fun projection(): ProjectionSnapshot {
        val root = JSONObject(get("/allsky/dsg-live-data.json"))
        val generated = parseInstant(root.opt("generated_at"))
        val camera = cameraFrom(root)
        return ProjectionSnapshot(generated, weatherFrom(root, generated, Instant.now()), camera)
    }

    internal fun cameraFrom(root: JSONObject): CameraSnapshot {
        val raw = root.optJSONObject("camera")?.opt("AS_CAMERAIMAGE") as? String
        val match = raw?.let { Regex("image-(20\\d{12})\\.jpg").matchEntire(it) }
        val shot = match?.groupValues?.get(1)?.let { cameraTimestampToInstant(it) }
        return CameraSnapshot(if (shot != null) raw else null, shot)
    }

    private fun cameraTimestampToInstant(value: String): Instant? = try {
        val local = java.time.LocalDateTime.parse(value, DateTimeFormatter.ofPattern("uuuuMMddHHmmss").withResolverStyle(ResolverStyle.STRICT))
        local.atZone(java.time.ZoneId.of("Europe/Rome")).toInstant()
    } catch (_: Exception) { null }

    internal fun weatherFrom(root: JSONObject, now: Instant): WeatherSnapshot = weatherFrom(root, parseInstant(root.opt("generated_at")), now)

    internal fun weatherFrom(root: JSONObject, generated: Instant?, now: Instant): WeatherSnapshot {
        val ageOk = generated != null && !generated.isAfter(now.plusSeconds(30)) &&
            !generated.isBefore(now.minusSeconds(150))
        val weather = root.optJSONObject("weather")
        val observed = parseInstant(weather?.opt("observed_at_utc"))
        val until = parseInstant(weather?.opt("fresh_until_utc"))
        val weatherValid = ageOk && observed != null && until != null &&
            !observed.isAfter(now.plusSeconds(30)) && until.isAfter(now)
        return WeatherSnapshot(
            generated, observed, until,
            if (weatherValid) bounded(number(weather, "temperature_c"), -80.0, 80.0) else null,
            if (weatherValid) bounded(number(weather, "humidity_pct"), 0.0, 100.0) else null,
            if (weatherValid) bounded(number(weather, "dew_point_c"), -100.0, 80.0) else null,
            if (weatherValid) bounded(number(weather, "wind_speed_kmh"), 0.0, 300.0) else null,
            weatherValid && listOf(
                number(weather, "temperature_c")?.let { bounded(it, -80.0, 80.0) },
                number(weather, "humidity_pct")?.let { bounded(it, 0.0, 100.0) },
                number(weather, "dew_point_c")?.let { bounded(it, -100.0, 80.0) },
                number(weather, "wind_speed_kmh")?.let { bounded(it, 0.0, 300.0) },
            ).all { it != null },
        )
    }

    internal fun archive(category: String): List<ArchiveItem> {
        val html = get(archivePath(category))
        return parseArchive(html, category)
    }

    internal fun meteorCandidates(): List<MeteorCandidate> = parseMeteorCatalog(get(meteorCatalogPath()))

    internal fun meteorCatalogPath(): String = "/allsky/meteors/"

    internal fun parseMeteorCatalog(html: String): List<MeteorCandidate> {
        val links = Regex("""href=['"]\./(meteors-20\d{12}\.jpg)['"]""", RegexOption.IGNORE_CASE)
        val formatter = DateTimeFormatter.ofPattern("uuuuMMddHHmmss").withResolverStyle(ResolverStyle.STRICT)
        return links.findAll(html).mapNotNull { match ->
            val file = match.groupValues[1]
            val local = runCatching { java.time.LocalDateTime.parse(file.removePrefix("meteors-").removeSuffix(".jpg"), formatter) }.getOrNull()
            local?.let { MeteorCandidate(file, it.atZone(java.time.ZoneId.of("Europe/Rome")).toInstant()) }
        }.distinctBy { it.file }.sortedByDescending { it.timestamp }.toList()
    }

    internal fun meteorMediaUrl(candidate: MeteorCandidate): String {
        require(candidate.file.matches(Regex("meteors-20\\d{12}\\.jpg")))
        val parsed = parseMeteorCatalog("<a href='./${candidate.file}'>candidate</a>")
        require(parsed.singleOrNull()?.file == candidate.file)
        return "$ORIGIN/allsky/meteors/${candidate.file}"
    }

    internal fun meteorThumbnailUrl(candidate: MeteorCandidate): String =
        meteorMediaUrl(candidate).replace("/meteors/", "/meteors/thumbnails/")

    internal fun archivePath(category: String): String = when (category) {
        "videos" -> "/allsky/videos/"
        "startrails" -> "/allsky/startrails/"
        "keograms" -> "/allsky/keograms/"
        else -> error("Unsupported archive category")
    }

    internal fun parseArchive(html: String, category: String): List<ArchiveItem> {
        archivePath(category)
        val link = Regex("href=['\"]\\./([A-Za-z0-9_-]+\\.(?:mp4|jpe?g))['\"]", RegexOption.IGNORE_CASE)
        val prefix = when (category) {
            "videos" -> "allsky-"
            "startrails" -> "startrails-"
            else -> "keogram-"
        }
        val extension = if (category == "videos") "mp4" else "jpg"
        return link.findAll(html).mapNotNull { match ->
            val file = match.groupValues[1]
            val date = file.removePrefix(prefix).removeSuffix(".$extension")
            if (file.startsWith(prefix) && validDate(date))
                ArchiveItem(date, file, category, extension) else null
        }.distinctBy { it.file }.sortedByDescending { it.date }.toList()
    }

    internal fun mediaUrl(item: ArchiveItem): String {
        require(item.category in setOf("videos", "startrails", "keograms"))
        val prefix = when (item.category) {
            "videos" -> "allsky-"
            "startrails" -> "startrails-"
            else -> "keogram-"
        }
        val ext = if (item.category == "videos") "mp4" else "jpg"
        require(item.file.matches(Regex("${Regex.escape(prefix)}20\\d{6}\\.${ext}")))
        require(validDate(item.file.removePrefix(prefix).removeSuffix(".$ext")))
        return "$ORIGIN/allsky/${item.category}/${item.file}"
    }

    private fun get(path: String): String {
        require(path in setOf("/allsky/dsg-live-data.json", "/allsky/videos/", "/allsky/startrails/", "/allsky/keograms/", meteorCatalogPath()))
        val connection = (URL(ORIGIN + path).openConnection() as HttpURLConnection).apply {
            requestMethod = "GET"
            connectTimeout = CONNECT_TIMEOUT_MS
            readTimeout = READ_TIMEOUT_MS
            instanceFollowRedirects = false
            setRequestProperty("Accept", if (path.endsWith(".json")) "application/json" else "text/html")
        }
        try {
            check(connection.responseCode == 200) { "HTTP ${connection.responseCode}" }
            val type = connection.contentType.orEmpty()
            check(if (path.endsWith(".json")) type.startsWith("application/json") else type.startsWith("text/html"))
            return connection.inputStream.use { stream ->
                val output = java.io.ByteArrayOutputStream()
                val buffer = ByteArray(8192)
                var total = 0
                while (true) {
                    val count = stream.read(buffer)
                    if (count < 0) break
                    total += count
                    check(total <= MAX_RESPONSE_BYTES) { "Response exceeds size limit" }
                    output.write(buffer, 0, count)
                }
                output.toString(Charsets.UTF_8.name())
            }
        } finally { connection.disconnect() }
    }

    private fun number(obj: JSONObject?, name: String): Double? {
        val value = obj?.opt(name)
        if (value !is Number) return null
        return value.toDouble().takeIf { it.isFinite() }
    }

    private fun bounded(value: Double?, minimum: Double, maximum: Double): Double? =
        value?.takeIf { it in minimum..maximum }

    private fun validDate(value: String): Boolean = try {
        value.matches(Regex("20\\d{6}")) && LocalDate.parse(value, DateTimeFormatter.ofPattern("uuuuMMdd").withResolverStyle(ResolverStyle.STRICT)) != null
    } catch (_: Exception) { false }

    private fun parseInstant(value: Any?): Instant? = try {
        when (value) {
            is Number -> Instant.ofEpochMilli((value.toDouble() * 1000).toLong())
            is String -> Instant.parse(value)
            else -> null
        }
    } catch (_: Exception) { null }
}

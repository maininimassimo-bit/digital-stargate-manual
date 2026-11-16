package it.digitalstargate.allskypocket

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.json.JSONObject
import org.junit.Test
import java.time.Instant

class AllskyRepositoryTest {
    @Test fun mediaPathsRemainInsideAllowedCatalogs() {
        assertEquals("$ORIGIN/allsky/videos/allsky-20261115.mp4", AllskyRepository.mediaUrl(ArchiveItem("20261115", "allsky-20261115.mp4", "videos", "mp4")))
        assertEquals("$ORIGIN/allsky/keograms/keogram-20261115.jpg", AllskyRepository.mediaUrl(ArchiveItem("20261115", "keogram-20261115.jpg", "keograms", "jpg")))
        listOf(
            ArchiveItem("20261115", "allsky-20261115.mp4", "meteors", "mp4"),
            ArchiveItem("20261115", "../private.jpg", "startrails", "jpg"),
            ArchiveItem("20261115", "allsky-20261115.mp4", "videos", "mp4").copy(file = "allsky-20261115.mp4?token=x"),
        ).forEach { item ->
            assertFalse(runCatching { AllskyRepository.mediaUrl(item) }.isSuccess)
        }
    }

    @Test fun requiredPublicPathsAndCategoryNamesAreExplicit() {
        assertTrue(ORIGIN.startsWith("https://"))
        assertFalse(ORIGIN.contains("@"))
        assertEquals(30_000L, POLL_INTERVAL_MS)
    }

    @Test fun projectionSelectsOnlyRequiredFreshWeatherValues() {
        val now = Instant.parse("2026-11-16T17:00:00Z")
        val json = JSONObject("""
            {"generated_at":1794848400,"meteors":{"secret":"ignored"},"pi":{"sensitive":"ignored"},"weather":{
              "temperature_c":15.6,"humidity_pct":76.7,"dew_point_c":11.5,"wind_speed_kmh":0,
              "observed_at_utc":"2026-11-16T16:59:30Z","fresh_until_utc":"2026-11-16T17:01:00Z"}}
        """.trimIndent())
        val weather = AllskyRepository.weatherFrom(json, Instant.parse("2026-11-16T16:59:50Z"), now)
        assertTrue(weather.fresh)
        assertEquals(0.0, weather.windKmh!!, 0.0)
        assertEquals(15.6, weather.temperatureC!!, 0.01)
    }

    @Test fun stalePartialOrFutureWeatherNeverBecomesZeroOrCurrent() {
        val now = Instant.parse("2026-11-16T17:00:00Z")
        val stale = JSONObject("""{"weather":{"temperature_c":0,"observed_at_utc":"2026-11-16T16:00:00Z","fresh_until_utc":"2026-11-16T16:01:00Z"}}""")
        val result = AllskyRepository.weatherFrom(stale, Instant.parse("2026-11-16T16:00:00Z"), now)
        assertFalse(result.fresh)
        assertEquals(null, result.temperatureC)
        val partial = JSONObject("""{"weather":{"temperature_c":0,"humidity_pct":50,"dew_point_c":4,"observed_at_utc":"2026-11-16T17:00:10Z","fresh_until_utc":"2026-11-16T17:01:00Z"}}""")
        assertFalse(AllskyRepository.weatherFrom(partial, now, now).fresh)
        val future = JSONObject("""{"weather":{"temperature_c":12,"humidity_pct":50,"dew_point_c":4,"wind_speed_kmh":3,"observed_at_utc":"2026-11-16T17:02:00Z","fresh_until_utc":"2026-11-16T17:03:00Z"}}""")
        assertFalse(AllskyRepository.weatherFrom(future, now, now).fresh)
    }

    @Test fun catalogsRejectOtherTypesAndInvalidDates() {
        val html = """
            <a href='./allsky-20261115.mp4'>ok</a>
            <a href='./allsky-20260230.mp4'>invalid date</a>
            <a href='./meteor-20261115.jpg'>excluded</a>
            <a href='../meteors/meteor-20261115.jpg'>excluded</a>
            <a href='./allsky-20261115.json'>excluded</a>
        """.trimIndent()
        assertEquals(listOf("allsky-20261115.mp4"), AllskyRepository.parseArchive(html, "videos").map { it.file })
        assertEquals(emptyList<ArchiveItem>(), AllskyRepository.parseArchive("", "startrails"))
        assertFalse(runCatching { AllskyRepository.archivePath("meteors") }.isSuccess)
    }

    @Test fun liveProjectionFreshnessUsesBoundariesAndRejectsMissingOrFutureTimes() {
        val now = Instant.parse("2026-11-16T17:00:00Z")
        assertTrue(isProjectionFresh(Instant.parse("2026-11-16T16:59:00Z"), now))
        assertTrue(isProjectionFresh(Instant.parse("2026-11-16T16:57:30Z"), now))
        assertFalse(isProjectionFresh(Instant.parse("2026-11-16T16:57:29Z"), now))
        assertFalse(isProjectionFresh(Instant.parse("2026-11-16T16:56:59Z"), now))
        assertFalse(isProjectionFresh(now.plusSeconds(31), now))
        assertFalse(isProjectionFresh(null, now))
        assertTrue(isCameraFresh(Instant.parse("2026-11-16T16:59:00Z"), now))
        assertFalse(isCameraFresh(Instant.parse("2026-11-16T16:56:59Z"), now))
        assertFalse(isCameraFresh(now.plusSeconds(31), now))
    }

    @Test fun cameraFilenameIsValidatedAndTranslatedFromRomeWallTime() {
        val valid = JSONObject("""{"camera":{"AS_CAMERAIMAGE":"image-20261116180000.jpg"},"meteors":{"ignored":true}}""")
        val camera = AllskyRepository.cameraFrom(valid)
        assertEquals("image-20261116180000.jpg", camera.fileName)
        assertEquals(Instant.parse("2026-11-16T17:00:00Z"), camera.shotAt)
        val invalid = JSONObject("""{"camera":{"AS_CAMERAIMAGE":"../meteors/image-20261116180000.jpg"}}""")
        assertEquals(null, AllskyRepository.cameraFrom(invalid).fileName)
        val invalidDate = JSONObject("""{"camera":{"AS_CAMERAIMAGE":"image-20260230120000.jpg"}}""")
        assertEquals(null, AllskyRepository.cameraFrom(invalidDate).shotAt)
    }
}

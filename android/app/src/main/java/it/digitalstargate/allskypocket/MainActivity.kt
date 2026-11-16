package it.digitalstargate.allskypocket

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.ui.graphics.Brush
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.viewinterop.AndroidView
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.Alignment
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.sp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.lifecycle.repeatOnLifecycle
import androidx.media3.common.MediaItem
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { PocketApp() }
    }
}

private val zone = ZoneId.of("Europe/Rome")
private val timeFormat = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss", java.util.Locale.ITALY).withZone(zone)
private val skyTop = Color(0xFF0B1B2D)
internal val skyPanel = Color(0xFF11263A)
private val aurora = Color(0xFF72E0CF)
private val starlight = Color(0xFFFFC77A)

@Composable
private fun NightSkyBackdrop(modifier: Modifier = Modifier) {
    Canvas(modifier.background(Brush.verticalGradient(listOf(Color(0xFF091625), Color(0xFF0B1725), Color(0xFF081321))))) {
        drawCircle(aurora.copy(alpha = 0.08f), radius = size.width * 0.46f, center = androidx.compose.ui.geometry.Offset(size.width * 0.82f, size.height * 0.12f))
        val points = listOf(0.08f to 0.09f, 0.23f to 0.16f, 0.72f to 0.08f, 0.91f to 0.26f, 0.16f to 0.36f, 0.84f to 0.48f, 0.06f to 0.68f, 0.94f to 0.76f, 0.39f to 0.84f, 0.68f to 0.94f)
        points.forEachIndexed { index, (x, y) -> drawCircle(if (index % 3 == 0) starlight.copy(alpha = 0.7f) else Color.White.copy(alpha = 0.45f), radius = if (index % 3 == 0) 1.8.dp.toPx() else 1.1.dp.toPx(), center = androidx.compose.ui.geometry.Offset(size.width * x, size.height * y)) }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun PocketApp() {
    val tabs = listOf("Live", "Meteo", "Archivio", "Meteore", "Mappa")
    var selected by remember { mutableIntStateOf(0) }
    MaterialTheme(colorScheme = darkColorScheme(
        primary = aurora, onPrimary = Color(0xFF062A2A), secondary = starlight,
        background = Color(0xFF081321), surface = Color(0xFF101F31), surfaceVariant = Color(0xFF1C3045),
        onSurface = Color(0xFFE5EEF8),
    )) {
        Scaffold(containerColor = MaterialTheme.colorScheme.background, topBar = { TopAppBar(title = {
            Column {
                Text("ALLSKY POCKET", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, letterSpacing = 1.5.sp)
                Text("DIGITAL STARGATE · MANCIANO", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.secondary)
            }
        }, colors = TopAppBarDefaults.topAppBarColors(containerColor = skyTop)) }, bottomBar = {
            NavigationBar { tabs.forEachIndexed { index, title ->
                NavigationBarItem(selected = selected == index, onClick = { selected = index },
                    icon = { Text(listOf("◉", "☼", "▤", "✦", "◎")[index]) }, label = { Text(title) })
            } }
        }) { padding ->
            Box(Modifier.fillMaxSize().padding(padding)) {
                NightSkyBackdrop(Modifier.fillMaxSize())
                when (selected) {
                    0 -> LiveScreen(active = true)
                    1 -> WeatherScreen(active = true)
                    2 -> ArchiveScreen()
                    3 -> MeteorsScreen()
                    else -> SkyMapScreen()
                }
            }
        }
    }
}

@Composable
private fun LiveScreen(active: Boolean) {
    val owner = LocalLifecycleOwner.current
    var visible by remember { mutableStateOf(owner.lifecycle.currentState.isAtLeast(Lifecycle.State.RESUMED)) }
    var updated by remember { mutableStateOf<Instant?>(null) }
    var shotAt by remember { mutableStateOf<Instant?>(null) }
    var cameraFileName by remember { mutableStateOf<String?>(null) }
    var error by remember { mutableStateOf<String?>(null) }
    var imageError by remember { mutableStateOf(false) }
    var imageNonce by remember { mutableIntStateOf(0) }
    var manualRefresh by remember { mutableIntStateOf(0) }
    var loading by remember { mutableStateOf(false) }
    DisposableEffect(owner) {
        val observer = androidx.lifecycle.LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_RESUME) visible = true
            if (event == Lifecycle.Event.ON_PAUSE) visible = false
        }
        owner.lifecycle.addObserver(observer)
        onDispose { owner.lifecycle.removeObserver(observer) }
    }
    LaunchedEffect(visible, active, manualRefresh) {
        if (!visible || !active) return@LaunchedEffect
        var backoff = POLL_INTERVAL_MS
        while (visible) {
            loading = true
            try {
                val data = withContext(Dispatchers.IO) { AllskyRepository.projection() }
                updated = data.generatedAt
                shotAt = data.camera.shotAt
                if (data.camera.fileName != null && data.camera.fileName != cameraFileName) {
                    cameraFileName = data.camera.fileName
                    imageNonce++
                }
                error = if (data.generatedAt == null) "Proiezione senza ora valida" else null
                backoff = POLL_INTERVAL_MS
            } catch (e: Exception) {
                error = "Connessione non disponibile: ${e.javaClass.simpleName}"
                backoff = (backoff * 2).coerceAtMost(5 * 60_000L)
            } finally { loading = false }
            delay(backoff)
        }
    }
    var showFull by remember { mutableStateOf(false) }
    var imageScale by remember { mutableFloatStateOf(1f) }
    var imageOffset by remember { mutableStateOf(Offset.Zero) }
    val imageFresh = isProjectionFresh(updated, Instant.now()) && isCameraFresh(shotAt, Instant.now())
    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(18.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Column(verticalArrangement = Arrangement.spacedBy(5.dp)) {
            Text("Il cielo, adesso", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
            Text("Manciano · Toscana · Allsky", color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        ElevatedCard(colors = CardDefaults.elevatedCardColors(containerColor = skyPanel), modifier = Modifier.fillMaxWidth()) {
            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("●", color = if (imageFresh && error == null) aurora else starlight)
                    Text(if (imageFresh && error == null) "PROIEZIONE AGGIORNATA" else "ULTIMO FOTOGRAMMA / NON AGGIORNATO", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.Bold)
                }
                Text("Ultimo aggiornamento dati  ${updated?.let(timeFormat::format) ?: "—"}", style = MaterialTheme.typography.bodySmall)
                Text("Scatto  ${shotAt?.let(timeFormat::format) ?: "ora non disponibile"}", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        ElevatedCard(colors = CardDefaults.elevatedCardColors(containerColor = Color.Black), modifier = Modifier.fillMaxWidth()) {
            Box(Modifier.fillMaxWidth().heightIn(min = 230.dp, max = if (showFull) 700.dp else 380.dp), contentAlignment = androidx.compose.ui.Alignment.Center) {
                PublicImage(key = imageNonce.toString(), url = "$ORIGIN/current/image.jpg?refresh=$imageNonce", description = "Ultimo fotogramma Allsky", onError = { imageError = it },
                    modifier = Modifier.fillMaxWidth().heightIn(min = 230.dp, max = if (showFull) 700.dp else 380.dp)
                        .pointerInput(showFull) { detectTransformGestures { _, pan, zoom, _ -> imageScale = (imageScale * zoom).coerceIn(1f, 5f); imageOffset += pan } }
                        .graphicsLayer(scaleX = imageScale, scaleY = imageScale, translationX = imageOffset.x, translationY = imageOffset.y))
                Text("✦", color = starlight, modifier = Modifier.align(androidx.compose.ui.Alignment.TopEnd).padding(12.dp))
            }
        }
        if (error != null || !imageFresh || imageError) Text(error ?: if (imageError) "Immagine non disponibile: verifica rete o risposta del server." else "La proiezione è scaduta; l’immagine può essere l’ultimo fotogramma disponibile.", color = MaterialTheme.colorScheme.error)
        Text("Il live è una successione di fotografie, non un flusso video.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            Button(onClick = { imageNonce++; manualRefresh++ }, enabled = !loading) { Text(if (loading) "Aggiorno…" else "Aggiorna") }
            OutlinedButton(onClick = { showFull = !showFull; imageScale = 1f; imageOffset = Offset.Zero }) { Text(if (showFull) "Adatta" else "Espandi") }
            Text("Zoom ${"%.1f".format(imageScale)}×", modifier = Modifier.align(androidx.compose.ui.Alignment.CenterVertically), color = aurora)
        }
    }
}

@Composable
private fun WeatherScreen(active: Boolean) {
    val owner = LocalLifecycleOwner.current
    var state by remember { mutableStateOf<WeatherSnapshot?>(null) }
    var error by remember { mutableStateOf<String?>(null) }
    var refresh by remember { mutableIntStateOf(0) }
    LaunchedEffect(owner, refresh, active) {
        if (!active) return@LaunchedEffect
        owner.lifecycle.repeatOnLifecycle(Lifecycle.State.RESUMED) {
            var delayMs = POLL_INTERVAL_MS
            while (true) {
                try {
                    val latest = withContext(Dispatchers.IO) { AllskyRepository.projection() }
                    state = latest.weather
                    error = null
                    delayMs = POLL_INTERVAL_MS
                }
                catch (e: Exception) { state = null; error = "Connessione non disponibile"; delayMs = (delayMs * 2).coerceAtMost(5 * 60_000L) }
                delay(delayMs)
            }
        }
    }
    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(18.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        Text("Aria e condizioni", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
        Text("Sensore CloudWatcher · Manciano", color = MaterialTheme.colorScheme.onSurfaceVariant)
        val value = state
        Text(if (error != null) error!! else if (value?.fresh == true) "Misura aggiornata" else "Misura non disponibile o scaduta",
            color = if (value?.fresh == true) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error)
        ElevatedCard(colors = CardDefaults.elevatedCardColors(containerColor = skyPanel), modifier = Modifier.fillMaxWidth()) {
            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
                Text("MISURA RICEVUTA", style = MaterialTheme.typography.labelLarge, color = starlight, fontWeight = FontWeight.Bold)
                Text("${value?.observedAt?.let(timeFormat::format) ?: "Ora non disponibile"}  ·  valida fino ${value?.freshUntil?.let(timeFormat::format) ?: "—"}", style = MaterialTheme.typography.bodySmall)
            }
        }
        WeatherValue("Temperatura", value?.temperatureC?.takeIf { value.fresh }, "°C")
        WeatherValue("Umidità", value?.humidityPct?.takeIf { value.fresh }, "%")
        WeatherValue("Punto di rugiada", value?.dewPointC?.takeIf { value.fresh }, "°C")
        WeatherValue("Vento", value?.windKmh?.takeIf { value.fresh }, "km/h")
        OutlinedButton(onClick = { refresh++ }) { Text("Aggiorna") }
    }
}

@Composable
private fun WeatherValue(name: String, value: Double?, unit: String) {
    ElevatedCard(Modifier.fillMaxWidth(), colors = CardDefaults.elevatedCardColors(containerColor = skyPanel)) { Row(Modifier.padding(18.dp).fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
        Text(name, color = MaterialTheme.colorScheme.onSurfaceVariant); Text(value?.let { "%.1f %s".format(it, unit) } ?: "—", fontWeight = FontWeight.Bold, color = aurora)
    } }
}

@Composable
private fun ArchiveScreen() {
    var category by remember { mutableStateOf("videos") }
    var items by remember { mutableStateOf<List<ArchiveItem>>(emptyList()) }
    var selectedIndex by remember { mutableIntStateOf(0) }
    var error by remember { mutableStateOf<String?>(null) }
    var loading by remember { mutableStateOf(false) }
    var reload by remember { mutableIntStateOf(0) }
    var fullImage by remember { mutableStateOf<ArchiveItem?>(null) }
    var videoError by remember { mutableStateOf<String?>(null) }
    val context = LocalContext.current
    var player by remember { mutableStateOf<ExoPlayer?>(null) }
    var current by remember { mutableStateOf<ArchiveItem?>(null) }
    DisposableEffect(player) {
        val ownedPlayer = player
        onDispose { ownedPlayer?.release() }
    }
    LaunchedEffect(category, reload) {
        loading = true; error = null; items = emptyList(); selectedIndex = 0; current = null
        player = null
        try { items = withContext(Dispatchers.IO) { AllskyRepository.archive(category) } }
        catch (e: kotlinx.coroutines.CancellationException) { throw e }
        catch (_: Exception) { error = "Catalogo non disponibile" }
        finally { loading = false }
    }
    Column(Modifier.fillMaxSize().padding(14.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text("Memoria del cielo", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
        Text("Prodotti pubblici · notti recenti", color = MaterialTheme.colorScheme.onSurfaceVariant)
        Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
            listOf("videos" to "Timelapse", "startrails" to "Startrail", "keograms" to "Keogrammi").forEach { (key, label) ->
                FilterChip(selected = category == key, onClick = {
                    if (category != key) { player = null; current = null; category = key }
                }, label = { Text(label) })
            }
        }
        val selected = items.getOrNull(selectedIndex)
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
            TextButton(enabled = selectedIndex > 0, onClick = { selectedIndex--; current = null; player = null }) { Text("‹ Precedente") }
            Text("${selected?.let { prettyDate(it.date) } ?: "—"}  ${if (items.isEmpty()) "" else "(${selectedIndex + 1}/${items.size})"}")
            TextButton(enabled = selectedIndex < items.lastIndex, onClick = { selectedIndex++; current = null; player = null }) { Text("Successiva ›") }
        }
        TextButton(onClick = { reload++ }, modifier = Modifier.align(Alignment.End)) { Text("Aggiorna catalogo") }
        if (loading) LinearProgressIndicator(Modifier.fillMaxWidth())
        if (error != null) Text(error!!, color = MaterialTheme.colorScheme.error)
        if (!loading && error == null && items.isEmpty()) Text("Nessun elemento disponibile.")
        Column(Modifier.weight(1f).verticalScroll(rememberScrollState()), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            selected?.let { item ->
                if (item.mediaType == "jpg") PublicImage(key = item.file, url = AllskyRepository.mediaUrl(item), description = "Apri immagine completa ${item.category} ${item.date}", modifier = Modifier.fillMaxWidth().heightIn(min = 180.dp, max = 620.dp).clickable { fullImage = item })
                else Row(Modifier.fillMaxWidth().clickable {
                    if (item.mediaType == "mp4") {
                        current = item
                        videoError = null
                        val codecSelector = object : androidx.media3.exoplayer.mediacodec.MediaCodecSelector {
                            override fun getDecoderInfos(
                                mimeType: String,
                                requiresSecureDecoder: Boolean,
                                requiresTunnelingDecoder: Boolean,
                            ) = androidx.media3.exoplayer.mediacodec.MediaCodecSelector.DEFAULT
                                .getDecoderInfos(mimeType, requiresSecureDecoder, requiresTunnelingDecoder)
                                .let { decoders ->
                                    if (mimeType == androidx.media3.common.MimeTypes.VIDEO_H264) {
                                        decoders.sortedByDescending { it.softwareOnly }
                                    } else decoders
                                }
                        }
                        val renderersFactory = androidx.media3.exoplayer.DefaultRenderersFactory(context)
                            .setMediaCodecSelector(codecSelector)
                            .setEnableDecoderFallback(true)
                        player = ExoPlayer.Builder(context, renderersFactory).build().also { p ->
                            p.addListener(object : androidx.media3.common.Player.Listener {
                                override fun onPlayerError(error: androidx.media3.common.PlaybackException) { videoError = "Video non riproducibile: ${error.errorCodeName}" }
                            })
                            p.setMediaItem(MediaItem.fromUri(AllskyRepository.mediaUrl(item))); p.prepare(); p.playWhenReady = true
                        }
                    }
                }.padding(14.dp), horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.CenterVertically) {
                    Text("▶  Riproduci timelapse ${prettyDate(item.date)}", modifier = Modifier.weight(1f), color = aurora)
                    if (current?.date == item.date) Text("Selezionato", color = MaterialTheme.colorScheme.primary)
                }
            }
            if (category == "videos" && selected != null && current?.date == selected.date) player?.let { p ->
                Text("Notte ${prettyDate(selected.date)}")
                AndroidView(factory = { PlayerView(it).apply { this.player = p; useController = true } }, update = { it.player = p }, modifier = Modifier.fillMaxWidth().height(230.dp))
            }
        }
    }
    if (videoError != null) AlertDialog(onDismissRequest = { videoError = null }, confirmButton = { TextButton(onClick = { videoError = null }) { Text("OK") } }, title = { Text("Errore video") }, text = { Text(videoError!!) })
    fullImage?.let { item ->
        androidx.compose.ui.window.Dialog(onDismissRequest = { fullImage = null }, properties = androidx.compose.ui.window.DialogProperties(usePlatformDefaultWidth = false)) {
            Surface(modifier = Modifier.fillMaxSize(), color = Color.Black) {
                Column(Modifier.fillMaxSize().padding(horizontal = 12.dp, vertical = 8.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("${if (item.category == "startrails") "Startrail" else "Keogramma"} · ${prettyDate(item.date)}", color = Color.White, style = MaterialTheme.typography.titleMedium)
                    PublicImage(key = "full-${item.file}", url = AllskyRepository.mediaUrl(item), description = "Immagine completa ${item.category} ${prettyDate(item.date)}", modifier = Modifier.fillMaxWidth().weight(1f))
                TextButton(onClick = { fullImage = null }) { Text("Chiudi") }
                }
            }
        }
    }
}

private fun prettyDate(date: String): String = try {
    "${date.substring(6, 8)}/${date.substring(4, 6)}/${date.substring(0, 4)}"
} catch (_: Exception) { date }

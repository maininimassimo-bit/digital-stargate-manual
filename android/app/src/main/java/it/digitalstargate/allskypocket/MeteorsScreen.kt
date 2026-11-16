package it.digitalstargate.allskypocket

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import java.util.Locale

private val meteorTimeFormat = DateTimeFormatter.ofPattern("dd/MM/yyyy · HH:mm:ss", Locale.ITALY)
    .withZone(ZoneId.of("Europe/Rome"))

@Composable
internal fun MeteorsScreen() {
    val context = LocalContext.current
    var candidates by remember { mutableStateOf<List<MeteorCandidate>>(emptyList()) }
    var error by remember { mutableStateOf<String?>(null) }
    var loading by remember { mutableStateOf(false) }
    var reload by remember { mutableIntStateOf(0) }
    var selected by remember { mutableStateOf<MeteorCandidate?>(null) }

    androidx.compose.runtime.LaunchedEffect(reload) {
        loading = true
        error = null
        try {
            candidates = withContext(Dispatchers.IO) { AllskyRepository.meteorCandidates() }
        } catch (e: kotlinx.coroutines.CancellationException) {
            throw e
        } catch (_: Exception) {
            error = localized(context, "Galleria meteore non disponibile. Verifica la connessione e riprova.", "Meteor gallery unavailable. Check your connection and try again.")
        } finally {
            loading = false
        }
    }

    Column(Modifier.fillMaxSize().padding(horizontal = 14.dp, vertical = 10.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text(localized("Meteore candidate", "Meteor candidates"), style = MaterialTheme.typography.headlineMedium)
        Text(localized("Segnalazioni automatiche da verificare: possono includere aerei, satelliti, riflessi o artefatti. Non sono conferme di meteore.", "Automated reports for review: they may include aircraft, satellites, reflections, or artifacts. They are not confirmed meteors."),
            style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Text(if (candidates.isEmpty()) localized("Galleria pubblica", "Public gallery") else localized("${candidates.size} immagini pubbliche", "${candidates.size} public images"), style = MaterialTheme.typography.labelLarge)
            TextButton(onClick = { reload++ }, enabled = !loading) { Text(localized("Aggiorna", "Refresh")) }
        }
        if (loading) LinearProgressIndicator(Modifier.fillMaxWidth())
        error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
        if (!loading && error == null && candidates.isEmpty()) Text(localized("Nessuna candidata pubblica disponibile.", "No public candidates available."))
        LazyColumn(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            items(candidates, key = { it.file }) { candidate ->
                ElevatedCard(
                    modifier = Modifier.fillMaxWidth().clickable { selected = candidate },
                    colors = CardDefaults.elevatedCardColors(containerColor = skyPanel),
                ) {
                    Row(Modifier.padding(8.dp), horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.CenterVertically) {
                        PublicImage(
                            key = "meteor-thumb-${candidate.file}",
                            url = AllskyRepository.meteorThumbnailUrl(candidate),
                            description = localized("Miniatura candidata ${meteorTimeFormat.format(candidate.timestamp)}", "Candidate thumbnail ${meteorTimeFormat.format(candidate.timestamp)}"),
                            modifier = Modifier.size(width = 112.dp, height = 66.dp),
                        )
                        Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
                            Text(meteorTimeFormat.format(candidate.timestamp), style = MaterialTheme.typography.titleSmall)
                            Text(localized("Candidata da verificare · apri immagine", "Candidate for review · open image"), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        }
    }

    selected?.let { candidate ->
        Dialog(onDismissRequest = { selected = null }, properties = DialogProperties(usePlatformDefaultWidth = false)) {
            androidx.compose.material3.Surface(Modifier.fillMaxSize(), color = Color.Black) {
                Column(Modifier.fillMaxSize().padding(horizontal = 12.dp, vertical = 8.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("${localized("Candidata da verificare", "Candidate for review")} · ${meteorTimeFormat.format(candidate.timestamp)}", color = Color.White, style = MaterialTheme.typography.titleMedium)
                    PublicImage(
                        key = "meteor-full-${candidate.file}",
                        url = AllskyRepository.meteorMediaUrl(candidate),
                        description = localized("Immagine della candidata ${meteorTimeFormat.format(candidate.timestamp)}", "Candidate image ${meteorTimeFormat.format(candidate.timestamp)}"),
                        modifier = Modifier.fillMaxWidth().weight(1f),
                    )
                    Text(localized("Questa segnalazione automatica non è una conferma scientifica.", "This automated report is not a scientific confirmation."), color = Color.LightGray, style = MaterialTheme.typography.bodySmall)
                    TextButton(onClick = { selected = null }) { Text(localized("Chiudi", "Close")) }
                }
            }
        }
    }
}

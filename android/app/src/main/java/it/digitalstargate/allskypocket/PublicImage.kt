package it.digitalstargate.allskypocket

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.mutableStateOf
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.unit.IntSize
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.draw.clipToBounds
import android.graphics.BitmapFactory
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.currentCoroutineContext
import kotlinx.coroutines.ensureActive
import kotlinx.coroutines.withContext
import java.net.HttpURLConnection
import java.net.URL

private const val IMAGE_CONNECT_TIMEOUT_MS = 8_000
private const val IMAGE_READ_TIMEOUT_MS = 12_000
private const val MAX_IMAGE_BYTES = 12_000_000
private const val MAX_THUMBNAIL_BYTES = 1_000_000

@Composable
internal fun PublicImage(key: String, url: String, description: String, onError: (Boolean) -> Unit = {}, modifier: Modifier = Modifier) {
    val target = remember(key) { mutableStateOf(IntSize.Zero) }
    val state = produceState<ImageLoadState>(ImageLoadState.Loading, key, url, target.value) {
        value = withContext(Dispatchers.IO) { loadImage(url, target.value.width.coerceAtLeast(640), target.value.height.coerceAtLeast(360)) }
    }.value
    androidx.compose.runtime.LaunchedEffect(state) { onError(state is ImageLoadState.Failed) }
    Box(modifier.clipToBounds().onSizeChanged { if (it.width > 0 && it.height > 0) target.value = it }, contentAlignment = Alignment.Center) {
        when (state) {
            ImageLoadState.Loading -> CircularProgressIndicator()
            is ImageLoadState.Ready -> Image(state.bitmap.asImageBitmap(), description, Modifier.fillMaxSize(), contentScale = ContentScale.Fit)
            is ImageLoadState.Failed -> Text(localized("Immagine non disponibile", "Image unavailable"), color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

private sealed interface ImageLoadState {
    data object Loading : ImageLoadState
    data class Ready(val bitmap: android.graphics.Bitmap) : ImageLoadState
    data class Failed(val reason: String) : ImageLoadState
}

private suspend fun loadImage(url: String, targetWidth: Int, targetHeight: Int): ImageLoadState {
    if (!url.matches(Regex("https://digitalstargate\\.freeddns\\.it:23232/(?:current/image\\.jpg\\?refresh=\\d+|allsky/(?:startrails/startrails|keograms/keogram)-20\\d{6}\\.jpg|allsky/meteors/(?:thumbnails/)?meteors-20\\d{12}\\.jpg)"))) {
        return ImageLoadState.Failed("Invalid image URL")
    }
    val connection = (URL(url).openConnection() as HttpURLConnection).apply {
        connectTimeout = IMAGE_CONNECT_TIMEOUT_MS
        readTimeout = IMAGE_READ_TIMEOUT_MS
        instanceFollowRedirects = false
    }
    return try {
        check(connection.responseCode == 200 && connection.url.toString() == url)
        check(connection.contentType.orEmpty().startsWith("image/jpeg"))
        val length = connection.contentLengthLong
        val byteLimit = if (url.contains("/thumbnails/")) MAX_THUMBNAIL_BYTES else MAX_IMAGE_BYTES
        check(length == -1L || length in 1..byteLimit.toLong())
        val bytes = connection.inputStream.use { stream ->
            val output = java.io.ByteArrayOutputStream(if (length > 0) length.toInt() else 64 * 1024)
            val buffer = ByteArray(16 * 1024)
            var total = 0
            while (true) {
                currentCoroutineContext().ensureActive()
                val count = stream.read(buffer)
                if (count < 0) break
                total += count
                check(total <= byteLimit)
                output.write(buffer, 0, count)
            }
            output.toByteArray()
        }
        val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        BitmapFactory.decodeByteArray(bytes, 0, bytes.size, bounds)
        val sample = calculateInSampleSize(bounds.outWidth, bounds.outHeight, targetWidth, targetHeight)
        val bitmap = BitmapFactory.decodeByteArray(bytes, 0, bytes.size, BitmapFactory.Options().apply { inSampleSize = sample }) ?: error("Invalid JPEG")
        ImageLoadState.Ready(bitmap)
    } catch (e: kotlinx.coroutines.CancellationException) {
        throw e
    } catch (e: Exception) {
        ImageLoadState.Failed(e.javaClass.simpleName)
    } finally { connection.disconnect() }
}

private fun calculateInSampleSize(width: Int, height: Int, targetWidth: Int, targetHeight: Int): Int {
    var sample = 1
    while (width / (sample * 2) >= targetWidth && height / (sample * 2) >= targetHeight) sample *= 2
    return sample
}

package it.digitalstargate.allskypocket

import android.annotation.SuppressLint
import android.net.Uri
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebChromeClient
import android.webkit.WebViewClient
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView

private const val MAP_URL = "$ORIGIN/allsky/"

private fun isAllowedMapResource(uri: Uri): Boolean =
    uri.scheme == "https" && uri.host == "digitalstargate.freeddns.it" && uri.port == 23232 && uri.userInfo == null

@SuppressLint("SetJavaScriptEnabled")
@Composable
internal fun SkyMapScreen() {
    val context = LocalContext.current
    var reload by remember { mutableIntStateOf(0) }
    var loading by remember { androidx.compose.runtime.mutableStateOf(true) }
    val webView = remember {
        WebView(context).apply {
            settings.javaScriptEnabled = true // Allsky's VirtualSky overlay is rendered by its own page scripts.
            // Allsky's page and VirtualSky use browser storage for page state and assets.
            settings.domStorageEnabled = true
            settings.allowFileAccess = false
            settings.allowContentAccess = false
            settings.javaScriptCanOpenWindowsAutomatically = false
            settings.setSupportMultipleWindows(false)
            settings.mixedContentMode = android.webkit.WebSettings.MIXED_CONTENT_NEVER_ALLOW
            settings.useWideViewPort = true
            settings.loadWithOverviewMode = true
            settings.builtInZoomControls = true
            settings.displayZoomControls = false
            setBackgroundColor(android.graphics.Color.TRANSPARENT)
            webChromeClient = WebChromeClient()
            android.webkit.CookieManager.getInstance().setAcceptThirdPartyCookies(this, false)
            webViewClient = object : WebViewClient() {
                override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean =
                    !isAllowedMapResource(request.url)

                override fun shouldInterceptRequest(view: WebView, request: WebResourceRequest): WebResourceResponse? =
                    if (isAllowedMapResource(request.url)) null else WebResourceResponse("text/plain", "UTF-8", null)

                override fun onPageStarted(view: WebView, url: String?, favicon: android.graphics.Bitmap?) {
                    loading = true
                }

                override fun onPageFinished(view: WebView, url: String?) {
                    loading = false
                    // Wait until Angular has attached its handler, then use the real page button.
                    // A synthetic click before Angular bootstrap is silently ignored.
                    view.evaluateJavascript(
                        "(function(){var n=0,t=setInterval(function(){var a=window.angular,b=document.getElementById('overlayBtn'),s=a&&b&&a.element(b).scope();if(b&&b.classList.contains('active')){clearInterval(t);return;}if(s&&typeof s.toggleOverlay==='function'){clearInterval(t);b.click();return;}if(++n>=80)clearInterval(t);},250);})()",
                        null,
                    )
                }
            }
            loadUrl(MAP_URL)
        }
    }
    LaunchedEffect(reload, webView) {
        if (reload > 0) {
            loading = true
            webView.reload()
        }
    }
    DisposableEffect(webView) {
        onDispose {
            webView.stopLoading()
            webView.destroy()
        }
    }
    Column(Modifier.fillMaxSize().padding(horizontal = 12.dp, vertical = 8.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        Text("Mappa celeste calibrata sul fotogramma live Allsky. I radianti degli sciami sono riferimenti del catalogo, non rilevazioni né previsioni verificate.",
            style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        if (loading) LinearProgressIndicator(Modifier.fillMaxWidth())
        OutlinedButton(onClick = { reload++ }, modifier = Modifier.fillMaxWidth()) { Text("Ricarica mappa e fotogramma") }
        AndroidView(factory = { webView }, modifier = Modifier.weight(1f).fillMaxWidth())
    }
}

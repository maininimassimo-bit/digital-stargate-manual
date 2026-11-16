package it.digitalstargate.allskypocket

import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalConfiguration
import android.content.Context
import java.util.Locale

/** Follows the Android app/system locale. Italian is native; other locales use English fallback. */
@Composable
internal fun localized(italian: String, english: String): String {
    val configuration = LocalConfiguration.current
    val language = configuration.locales[0]?.language ?: Locale.getDefault().language
    return if (language.equals("it", ignoreCase = true)) italian else english
}

internal fun localized(context: Context, italian: String, english: String): String {
    val language = context.resources.configuration.locales[0]?.language ?: Locale.getDefault().language
    return if (language.equals("it", ignoreCase = true)) italian else english
}

@Composable
internal fun localizedLanguageName(): String {
    val configuration = LocalConfiguration.current
    val language = configuration.locales[0] ?: Locale.getDefault()
    return if (language.language.equals("it", ignoreCase = true)) "Italiano" else "English"
}

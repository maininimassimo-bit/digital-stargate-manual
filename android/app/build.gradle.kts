plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "it.digitalstargate.allskypocket"
    compileSdk = 36

    defaultConfig {
        applicationId = "it.digitalstargate.allskypocket"
        minSdk = 26
        targetSdk = 36
        versionCode = 8
        versionName = "0.2.6"
    }

    signingConfigs {
        create("playUpload") {
            val uploadStoreFile = providers.gradleProperty("playUploadStoreFile").orNull
            val uploadStorePassword = providers.gradleProperty("playUploadStorePassword").orNull
            val uploadKeyAlias = providers.gradleProperty("playUploadKeyAlias").orNull
            val uploadKeyPassword = providers.gradleProperty("playUploadKeyPassword").orNull
            if (uploadStoreFile != null && uploadStorePassword != null && uploadKeyAlias != null && uploadKeyPassword != null) {
                storeFile = file(uploadStoreFile)
                storePassword = uploadStorePassword
                keyAlias = uploadKeyAlias
                keyPassword = uploadKeyPassword
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            if (listOf("playUploadStoreFile", "playUploadStorePassword", "playUploadKeyAlias", "playUploadKeyPassword")
                    .all { providers.gradleProperty(it).isPresent }) {
                signingConfig = signingConfigs.getByName("playUpload")
            }
        }
    }
    buildFeatures {
        compose = true
        buildConfig = true
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
}

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2025.10.00")
    implementation(composeBom)
    androidTestImplementation(composeBom)
    implementation("androidx.activity:activity-compose:1.11.0")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.foundation:foundation")
    implementation("androidx.compose.foundation:foundation-layout")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.9.4")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.9.4")
    implementation("androidx.media3:media3-exoplayer:1.8.0")
    implementation("androidx.media3:media3-ui:1.8.0")
    debugImplementation("androidx.compose.ui:ui-tooling")
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.json:json:20260814")
}

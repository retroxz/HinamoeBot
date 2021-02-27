plugins {
    val kotlinVersion = "1.4.20"
    kotlin("jvm") version kotlinVersion
    kotlin("plugin.serialization") version kotlinVersion

    id("net.mamoe.mirai-console") version "2.0-RC" // mirai-console version
}

mirai {
    coreVersion = "2.0-RC" // mirai-core version

}

kotlin.sourceSets.all { languageSettings.useExperimentalAnnotation("kotlin.RequiresOptIn") }

group = "HinaMoe-plugin-nbnhhsh"
version = "1.0.0"

repositories {
    mavenLocal()
    jcenter()
    mavenCentral()
}

dependencies {
    implementation ("com.squareup.okhttp3:okhttp:4.2.1")
    implementation ("com.alibaba:fastjson:1.2.71")
}
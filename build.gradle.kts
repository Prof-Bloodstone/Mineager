plugins {
    application
    kotlin("jvm") version "1.4.10"
    id("com.github.johnrengelman.shadow") version "6.1.0"
}

group = "dev.bloodstone.mineager"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.seleniumhq.selenium:selenium-java:4.0.0-alpha-7")
    implementation("org.jetbrains.kotlin:kotlin-stdlib")
    implementation("io.github.microutils:kotlin-logging-jvm:2.0.2")
    implementation("info.picocli:picocli:4.5.2")
    implementation("io.github.bonigarcia:webdrivermanager:4.2.2")
    implementation("org.slf4j:slf4j-log4j12:1.7.29")
}

plugins {
    kotlin("jvm") version "1.4.10"

}




tasks {
    named<com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar>("shadowJar") {
        archiveBaseName.set("demo")
        mergeServiceFiles()
    }

    shadowJar {
        // Minimizing breaks log4j, java.lang.ClassNotFoundException: org.apache.log4j.ConsoleAppender
       // minimize()
    }
}


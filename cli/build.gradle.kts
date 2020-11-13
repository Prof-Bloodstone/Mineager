plugins {
  application
  kotlin("jvm")
  id("com.github.johnrengelman.shadow") version "6.1.0"
}

application {
  mainClass.set("${group}.${name}.MainKt")
}

dependencies {
  implementation(project(":core"))
  compile("info.picocli:picocli:4.5.2")
  implementation("io.github.microutils:kotlin-logging-jvm:2.0.2")
}

tasks {
  named<com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar>("shadowJar") {
    archiveBaseName.set("demo")
    mergeServiceFiles()
  }

  shadowJar {
    // Minimizing breaks log4j, java.lang.ClassNotFoundException: org.apache.log4j.ConsoleAppender
    // Need to add explicit excludes for minimization
   // minimize()
  }
}

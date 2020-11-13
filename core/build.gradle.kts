plugins {
  `java-library`
  kotlin("jvm")
}

dependencies {
  implementation("org.seleniumhq.selenium:selenium-java:4.0.0-alpha-7")
  implementation("org.jetbrains.kotlin:kotlin-stdlib")
  implementation("io.github.microutils:kotlin-logging-jvm:2.0.2")
  implementation("io.github.bonigarcia:webdrivermanager:4.2.2")
  implementation("org.slf4j:slf4j-log4j12:1.7.29")
}

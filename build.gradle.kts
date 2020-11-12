plugins {
  base
  kotlin("jvm") version "1.4.10" apply false
}

allprojects {
  group = "dev.bloodstone.mineager"
  version = "1.0.0-SNAPSHOT"
  repositories {
    jcenter()
  }
}

dependencies {
    // Make the root project archives configuration depend on every sub-project
    subprojects.forEach {
        archives(it)
    }
}

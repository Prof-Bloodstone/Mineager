plugins {
    application
    kotlin("jvm")
}

repositories {
    mavenCentral()
}

application {
    mainClass.set("${group}.${name}.MainKt")
}

dependencies {
    implementation(project(":core"))
    compile("info.picocli:picocli:4.5.2")
}

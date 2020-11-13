import org.gradle.api.Project

import org.gradle.kotlin.dsl.*

// Not used anywhere yet
fun Project.kotlinProject() {
    dependencies {
        "compile"(kotlin("jvm"))
    }
}


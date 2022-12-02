plugins {
    kotlin("jvm") version "1.7.20"
}

group = "nl.testmerrie.aoc2022"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

kotlin {
    sourceSets {
        main {
            dependencies {
                implementation("org.jetbrains.kotlinx:kotlinx-cli:0.3.5")
            }
        }
    }
}

tasks {
    sourceSets {
        main {
            java.srcDirs("src")
        }
    }
}

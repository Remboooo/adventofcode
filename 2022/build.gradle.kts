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
                implementation("org.jetbrains.kotlinx:multik-core:0.2.0")
                implementation("org.jetbrains.kotlinx:multik-default:0.2.0")
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

import kotlinx.cli.*
import java.io.File

data class Dir(val parent: Dir?, var size: Int)

val DIR_RE = """(\d+) .+""".toRegex()

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 7 part 1")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val root = Dir(null, 0)
    val allDirs = mutableListOf(root)
    var currentDir = root

    File(input).readLines().forEach {line ->
        when {
            line == "\$ cd /" -> currentDir = root
            line == "\$ cd .." -> currentDir = currentDir.parent!!
            line.startsWith("\$ cd") -> {
                // bold assumption: we never cd into the same dir twice
                currentDir = Dir(currentDir, 0)
                allDirs.add(currentDir)
            }
            else -> {
                val match = DIR_RE.matchEntire(line)
                if (match != null) {
                    val fileSize = match.groupValues[1].toInt()
                    var affectedDir: Dir? = currentDir
                    while (affectedDir != null) {
                        affectedDir.size += fileSize
                        affectedDir = affectedDir.parent
                    }
                }
            }
        }
    }
    println(allDirs.filter{ it.size <= 100000}.sumOf { it.size })

}

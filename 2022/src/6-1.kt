import kotlinx.cli.*
import util.transpose
import java.io.File

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 6 part 1")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    File(input).readLines().forEach { line ->
        println(line.windowed(4).mapIndexed { i, s ->
            if (s.all { c -> s.count { it == c } == 1 }) i+4 else null
        }.find { it != null })
    }
}

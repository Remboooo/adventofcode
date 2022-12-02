import kotlinx.cli.ArgParser
import kotlinx.cli.ArgType
import java.io.File

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 1 part 2")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val currentBest = mutableListOf<Int>()
    File(input).readLines().fold(0) { current, line ->
        if (line.isBlank()) { currentBest.add(current); 0 }
        else current + line.toInt()
    }

    println(currentBest.sortedDescending().slice(0..2).sum())
}
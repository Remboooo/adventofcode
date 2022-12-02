import kotlinx.cli.*
import java.io.File
import kotlin.math.max

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 1 part 1")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    println(
        File(input).readLines().fold(Pair(0, 0)) { (currentMax, current), line ->
            if (line.isBlank()) Pair(max(currentMax, current), 0)
            else Pair(currentMax, current + line.toInt())
        }.first
    )
}
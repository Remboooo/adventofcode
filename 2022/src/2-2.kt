import kotlinx.cli.*
import java.io.File
import kotlin.math.max

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 2 part 2")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val points = mapOf(
        "A X" to 3+0, "A Y" to 1+3, "A Z" to 2+6,
        "B X" to 1+0, "B Y" to 2+3, "B Z" to 3+6,
        "C X" to 2+0, "C Y" to 3+3, "C Z" to 1+6,
    )

    println(File(input).readLines().sumOf { points[it]!! })
}
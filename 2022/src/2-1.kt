import kotlinx.cli.*
import java.io.File
import kotlin.math.max

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 2 part 1")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val lines = File(input).readLines()

    val shapePoints = mapOf('X' to 1, 'Y' to 2, 'Z' to 3)
    val winIf = mapOf('X' to 'C', 'Z' to 'B', 'Y' to 'A')
    val drawIf = mapOf('X' to 'A', 'Y' to 'B', 'Z' to 'C')

    var score = 0
    for (line in lines) {
        val me = line.toCharArray()[2]
        val them = line.toCharArray()[0]

        score += shapePoints[me]!!

        if (winIf[me]!! == them) {
            score += 6
        }
        else if (drawIf[me]!! == them) {
            score += 3
        }
    }

    println(score)
}
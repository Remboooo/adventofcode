import kotlinx.cli.*
import java.io.File

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 2 part 1")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val shapePoints = mapOf('X' to 1, 'Y' to 2, 'Z' to 3)
    val winIf = mapOf('X' to 'C', 'Z' to 'B', 'Y' to 'A')
    val drawIf = mapOf('X' to 'A', 'Y' to 'B', 'Z' to 'C')

    println(
        File(input).readLines().sumOf {
            val (them, _, me) = it.toCharArray()
            shapePoints[me]!! + when(them) {
                winIf[me]!! -> 6
                drawIf[me]!! -> 3
                else -> 0
            }
        }
    )
}
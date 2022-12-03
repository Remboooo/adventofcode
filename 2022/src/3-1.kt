import kotlinx.cli.*
import java.io.File
import kotlin.math.max

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 3 part 1")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    println(
        File(input).readLines().sumOf {line ->
            val upper = line.substring(0 until line.length/2)
            val lower = line.substring(line.length/2 until line.length)
            val common = upper.toCharArray().first { lower.contains(it) }
            if (('A'..'Z').contains(common)) {
                27 + (common - 'A')
            } else {
                1 + (common - 'a')
            }
        }
    )
}
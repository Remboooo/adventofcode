import kotlinx.cli.*
import java.io.File
import kotlin.math.max

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 3 part 2")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    println(
        File(input).readLines().chunked(3).sumOf {lines ->
            val common = lines[0].toCharArray().first {
                lines[1].contains(it) && lines[2].contains(it)
            }
            if (('A'..'Z').contains(common)) {
                27 + (common - 'A')
            } else {
                1 + (common - 'a')
            }
        }
    )
}
import kotlinx.cli.ArgParser
import kotlinx.cli.ArgType
import util.*
import java.io.File
import kotlin.math.absoluteValue
import kotlin.math.sign

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 9 part 2")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val knots = (0..9).map { XY(0, 0) }.toMutableList()

    val tailTrail = mutableSetOf(knots.last())

    for ((dir, amount) in File(input).readLines().map { line -> Pair(line[0], line.substring(2).toInt())}) {
        repeat(amount) {
            when (dir) {
                'U' -> knots[0] += XY(0, -1)
                'D' -> knots[0] += XY(0, +1)
                'L' -> knots[0] += XY(-1, 0)
                'R' -> knots[0] += XY(+1, 0)
            }
            for (i in (0 until knots.size-1)) {
                val diff = knots[i] - knots[i+1]
                if (diff.x == 0 && diff.y.absoluteValue > 1) {
                    knots[i+1] += XY(0, diff.y.sign)
                } else if (diff.y == 0 && diff.x.absoluteValue > 1) {
                    knots[i+1] += XY(diff.x.sign, 0)
                } else if (diff.x.absoluteValue > 1 || diff.y.absoluteValue > 1) {
                    knots[i+1] += XY(diff.x.sign, diff.y.sign)
                }
            }
            tailTrail.add(knots.last())
        }
    }
    println(tailTrail.size)
}

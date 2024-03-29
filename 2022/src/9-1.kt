import kotlinx.cli.ArgParser
import kotlinx.cli.ArgType
import util.*
import java.io.File
import kotlin.math.absoluteValue
import kotlin.math.sign

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 9 part 1")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    var head = XY(0, 0)
    var tail = head

    val tailTrail = mutableSetOf(tail)

    for ((dir, amount) in File(input).readLines().map { line -> Pair(line[0], line.substring(2).toInt())}) {
        repeat(amount) {
            when (dir) {
                'U' -> head += XY(0, -1)
                'D' -> head += XY(0, +1)
                'L' -> head += XY(-1, 0)
                'R' -> head += XY(+1, 0)
            }
            val diff = head - tail
            if (diff.x == 0 && diff.y.absoluteValue > 1) {
                tail += XY(0, diff.y.sign)
            }
            else if (diff.y == 0 && diff.x.absoluteValue > 1) {
                tail += XY(diff.x.sign, 0)
            }
            else if (diff.x.absoluteValue > 1 || diff.y.absoluteValue > 1) {
                tail += XY(diff.x.sign, diff.y.sign)
            }
            tailTrail.add(tail)
        }
    }
    println(tailTrail.size)
}

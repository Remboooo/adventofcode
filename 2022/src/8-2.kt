import kotlinx.cli.ArgParser
import kotlinx.cli.ArgType
import org.jetbrains.kotlinx.multik.api.mk
import org.jetbrains.kotlinx.multik.api.ndarray
import org.jetbrains.kotlinx.multik.api.ones
import org.jetbrains.kotlinx.multik.api.zeros
import org.jetbrains.kotlinx.multik.ndarray.data.D2Array
import org.jetbrains.kotlinx.multik.ndarray.data.get
import org.jetbrains.kotlinx.multik.ndarray.data.set
import org.jetbrains.kotlinx.multik.ndarray.operations.max
import util.reversedAxis
import java.io.File

private fun viewingDistanceToRight(grid: D2Array<Int>, scores: D2Array<Int>) {
    val h = grid.shape[0]
    val w = grid.shape[1]
    for (y in (0 until h)) {
        for (x in (0 until w)) {
            val vh = grid[y, x]
            scores[y, x] *= (x+1 until w)
                .mapIndexed { d, vx -> if (vx == w - 1 || grid[y, vx] >= vh) d+1 else null }
                .firstOrNull() { it != null } ?: 0
        }
    }
}

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 8 part 2")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val grid = mk.ndarray(File(input).readLines().map { it.toCharArray().map { c -> c.digitToInt() }})
    val scores = mk.ones<Int>(grid.shape[0], grid.shape[1])

    viewingDistanceToRight(grid, scores)
    viewingDistanceToRight(grid.reversedAxis(1), scores.reversedAxis(1))
    viewingDistanceToRight(grid.transpose(), scores.transpose())
    viewingDistanceToRight(grid.reversedAxis(0).transpose(), scores.reversedAxis(0).transpose())

    println(scores.max())
}

import kotlinx.cli.ArgParser
import kotlinx.cli.ArgType
import org.jetbrains.kotlinx.multik.api.mk
import org.jetbrains.kotlinx.multik.api.ndarray
import org.jetbrains.kotlinx.multik.api.zeros
import org.jetbrains.kotlinx.multik.ndarray.data.D2Array
import org.jetbrains.kotlinx.multik.ndarray.data.get
import org.jetbrains.kotlinx.multik.ndarray.data.set
import org.jetbrains.kotlinx.multik.ndarray.operations.count
import util.reversedAxis
import java.io.File

private const val FROM_LEFT = 1
private const val FROM_RIGHT = 2
private const val FROM_TOP = 4
private const val FROM_BOTTOM = 8

private fun visibilityFromLeft(grid: D2Array<Int>, visibility: D2Array<Int>, marker: Int) {
    val h = grid.shape[0]
    val w = grid.shape[1]
    for (y in (0 until h)) {
        var threshold = -1
        for (x in (0 until w)) {
            if (grid[y, x] > threshold) {
                threshold = grid[y, x]
                visibility[y, x] += marker
            }
        }
    }
}

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 8 part 1")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val grid = mk.ndarray(File(input).readLines().map { it.toCharArray().map { c -> c.digitToInt() }})
    val visible = mk.zeros<Int>(grid.shape[0], grid.shape[1])

    visibilityFromLeft(grid, visible, FROM_LEFT)
    visibilityFromLeft(grid.reversedAxis(1), visible.reversedAxis(1), FROM_RIGHT)
    visibilityFromLeft(grid.transpose(), visible.transpose(), FROM_TOP)
    visibilityFromLeft(grid.reversedAxis(0).transpose(), visible.reversedAxis(0).transpose(), FROM_BOTTOM)

    println(visible.count { it != 0 })
}

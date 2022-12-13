import kotlinx.cli.ArgParser
import kotlinx.cli.ArgType
import org.jetbrains.kotlinx.multik.api.mk
import org.jetbrains.kotlinx.multik.api.ndarray
import org.jetbrains.kotlinx.multik.ndarray.operations.map
import util.*
import java.io.File

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 12 part 2")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val lines = File(input).readLines()

    val heights = mk.ndarray(
        lines.map { line -> line.toCharArray().map {
            when(it) {
                'S' -> 0
                'E' -> 26
                else -> it-'a'
            }
        }}
    )

    val bounds = heights.bounds()
    val end = lines.coordsOf('E').first()

    val distances = heights.map { Int.MAX_VALUE }
    distances[end] = 0

    // Dijkstra that shit
    val nearest = fun(): XY? {
        val q = mutableListOf(end)
        while (q.isNotEmpty()) {
            val xy = q.removeFirst()
            val dist = distances[xy]
            val neighbours = xy.neighbours(bounds).filter { heights[it] >= heights[xy] - 1 }
            for (neighbour in neighbours) {
                if (distances[neighbour] > dist + 1) {
                    distances[neighbour] = dist + 1
                    if (heights[neighbour] == 0) return neighbour
                    q.add(neighbour)
                }
            }
        }
        return null
    }()!!

    println(distances[nearest])
}

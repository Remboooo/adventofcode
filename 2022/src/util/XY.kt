package util

import org.jetbrains.kotlinx.multik.ndarray.data.D2
import org.jetbrains.kotlinx.multik.ndarray.data.MultiArray

typealias XY = Pair<Int,Int>
val XY.y: Int get() = this.first
val XY.x: Int get() = this.second

fun XY.neighbours(bounds: Bounds): List<XY> {
    return listOf(
        XY(-1, 0), XY(+1, 0), XY(0, -1), XY(0, +1)
    ).map { this + it }.filter { bounds.contains(it) }
}

data class Bounds(val minX: Int = 0, val minY: Int = 0, val maxX: Int, val maxY: Int) {
    fun contains(xy: XY): Boolean {
        return xy.x in minX..maxX && xy.y in minY..maxY
    }
}

fun <T> MultiArray<T, D2>.bounds(): Bounds {
    return Bounds(maxX=shape[1]-1, maxY=shape[0]-1)
}

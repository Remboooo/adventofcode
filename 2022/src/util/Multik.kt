package util

import org.jetbrains.kotlinx.multik.ndarray.data.*
import org.jetbrains.kotlinx.multik.ndarray.operations.forEachMultiIndexed

fun <T> D2Array<T>.reversedAxis(axis: Int): D2Array<T> {
    val newStrides = strides.copyOf()
    newStrides[axis] = -strides[axis]
    val newOffset = offset + strides[axis] * (shape[axis]-1)
    return NDArray(this.data, newOffset, shape.copyOf(), newStrides, this.dim, base = base ?: this)
}

operator fun <T> MultiArray<T, D2>.get(ind: Pair<Int, Int>): T {
    return this[ind.first, ind.second]
}

operator fun <T> MutableMultiArray<T, D2>.set(ind: Pair<Int, Int>, v: T) {
    this[ind.first, ind.second] = v
}

fun <T> MultiArray<T, D2>.coordsOf(item: T): List<Pair<Int,Int>> {
    val result = mutableListOf<Pair<Int,Int>>()
    this.forEachMultiIndexed { index, t -> if (t == item) result.add(Pair(index[0], index[1])) }
    return result.toList()
}

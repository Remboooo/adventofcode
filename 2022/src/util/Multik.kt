package util

import org.jetbrains.kotlinx.multik.ndarray.data.D2Array
import org.jetbrains.kotlinx.multik.ndarray.data.NDArray

fun <T> D2Array<T>.reversedAxis(axis: Int): D2Array<T> {
    val newStrides = strides.copyOf()
    newStrides[axis] = -strides[axis]
    val newOffset = offset + strides[axis] * (shape[axis]-1)
    return NDArray(this.data, newOffset, shape.copyOf(), newStrides, this.dim, base = base ?: this)
}

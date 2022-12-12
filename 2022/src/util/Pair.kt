package util

operator fun Pair<Int,Int>.plus(other: Pair<Int,Int>): Pair<Int,Int> {
    return Pair(first+other.first, second+other.second)
}

operator fun Pair<Int,Int>.minus(other: Pair<Int,Int>): Pair<Int,Int> {
    return Pair(first-other.first, second-other.second)
}

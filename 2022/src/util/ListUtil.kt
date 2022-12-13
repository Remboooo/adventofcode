package util

fun <A> List<A>.toPair(): Pair<A,A> {return zipWithNext().single()}
fun <T> Iterable<Iterable<T>>.transpose(): List<List<T>> {
    // This feels like it should be a fold operation, but it took longer than 2 sips of beer
    // so I could not be arsed rethinking this one just yet
    val outer = this.toList()
    if (outer.isEmpty()) return emptyList()
    val result = outer[0].map { mutableListOf(it) }
    outer.drop(1).forEach {
        it.forEachIndexed { i, elem -> result[i].add(elem) }
    }
    return result.map { it.toList() }
}

fun Iterable<String>.coordsOf(item: Char): List<Pair<Int,Int>> {
    return flatMapIndexed { y, line -> line.mapIndexed { x, c ->
        if (c == item) Pair(y, x) else null
    }}.filterNotNull()
}

fun <T> Iterable<Iterable<T>>.coordsOf(item: T): List<Pair<Int,Int>> {
    return flatMapIndexed { y, line -> line.mapIndexed { x, c ->
        if (c == item) Pair(x, y) else null
    }}.filterNotNull()
}

fun <E> MutableList<E>.removeLast(amount: Int): List<E> {
    val toRemove = subList(size-amount, size).toList()
    repeat(amount) { removeLast() }
    return toRemove
}

fun Iterable<Iterable<Int>>.toPixels(): String {
    return joinToString("\n") {
        it.map {
            when (it) {
                1 -> '#'
                else -> ' '
            }
        }.joinToString("")
    }
}

inline fun <T> Iterable<T>.productOf(selector: (T) -> Int): Int {
    return map(selector).reduce { a, b -> a*b }
}

fun Iterable<Int>.product(): Int {
    return reduce { a, b -> a*b }
}

fun Iterable<Long>.product(): Long {
    return reduce { a, b -> a*b }
}
package util

fun <A> List<A>.toPair(): Pair<A,A> {return zipWithNext().single()}
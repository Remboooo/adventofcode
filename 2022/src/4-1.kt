import kotlinx.cli.*
import java.io.File
import kotlin.math.max

fun Pair<Int,Int>.toMask(): Int {
    var result = 0
    for (i in 0..63) {
        if (i >= this.first && i <= this.second) result = result or 1
        result = result shl 1
    }
    return result
}

class Assignment(p: IntRange) {
    val lsb = 0..63
}

fun Pair<Int,Int>.toRange(): IntRange {return first..second}
fun <A> List<A>.toPair(): Pair<A,A> {return zipWithNext().single()}

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 4 part 1")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val ranges = File(input).readLines()
        .map {it.split(',')}
        .map { elf -> elf.map {it.split('-').map { s -> s.toInt()}.toPair().toRange()}.toPair()}

//    ranges.map {
//        val intersection = it.first.intersect(it.second)
//        it.first.to
//    }

    println(Pair(1, 2).toMask())

    println(ranges)
}

import kotlinx.cli.*
import util.removeLast
import util.transpose
import java.io.File

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 5 part 2")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val lines = File(input).readLines()
    val crateLines = lines.takeWhile { it.contains('[') }
    val crateLineLength = crateLines.maxOf { it.length }
    val piles = crateLines
        .map { it.padEnd(crateLineLength, ' ') }
        .map { it.toCharArray().filterIndexed { i, _ -> (i-1)%4==0 }}
        .transpose()
        .map { it.filter { c -> c != ' ' }.reversed().toMutableList() }

    val ops = lines
        .drop(crateLines.size+2)
        .map { OP_RE.matchEntire(it)!!.groupValues.drop(1).map { g -> g.toInt() } }
        .map { Op(it[0], it[1], it[2])}

    for (op in ops) {
       piles[op.to - 1].addAll(piles[op.from - 1].removeLast(op.amount))
    }

    println(piles.map { it.last() }.joinToString(""))
}

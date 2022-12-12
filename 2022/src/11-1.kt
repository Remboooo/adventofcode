import kotlinx.cli.ArgParser
import kotlinx.cli.ArgType
import util.product
import util.productOf
import java.io.File
import java.lang.IllegalArgumentException


data class Monkey(
    var items: MutableList<Long>,
    val op: Char,
    val operand: Long?,
    val testDivisor: Long,
    val trueMonkey: Int,
    val falseMonkey: Int,
    var inspects: Long = 0
) {
}

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 11 part 1")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val monkeys = File(input).readLines().chunked(7).map {lines ->
        Monkey(
            items = lines[1].substring("  Starting items: ".length).split(", ").map { it.toLong() }.toMutableList(),
            op = lines[2]["  Operation: new = old ".length],
            operand = lines[2].substring("  Operation: new = old util.getX ".length).toLongOrNull(),
            testDivisor = lines[3].substring("  Test: divisible by ".length).toLong(),
            trueMonkey = lines[4].substring("    If true: throw to monkey ".length).toInt(),
            falseMonkey = lines[5].substring("    If false: throw to monkey ".length).toInt()
        )
    }

    println(monkeys.joinToString("\n"))

    for (round in (1..20)) {
        for (monkey in monkeys) {
            for (item in monkey.items) {
                monkey.inspects++
                var newVal = item
                when (monkey.op) {
                    '+' -> newVal += (monkey.operand ?: item)
                    '*' -> newVal *= (monkey.operand ?: item)
                }
                newVal /= 3
                monkeys[
                    if (newVal % monkey.testDivisor == 0L) monkey.trueMonkey else monkey.falseMonkey
                ].items.add(newVal)
            }
            monkey.items.clear()
        }
    }

    println("End result:")
    println(monkeys.joinToString("\n"))

    println(monkeys.map { it.inspects }.sortedDescending().take(2).product())
}

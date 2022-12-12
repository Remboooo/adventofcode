import kotlinx.cli.ArgParser
import kotlinx.cli.ArgType
import util.product
import util.productOf
import java.io.File
import java.lang.IllegalArgumentException

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 11 part 2")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val monkeys = File(input).readLines().chunked(7).map {lines ->
        Monkey(
            items = lines[1].substring("  Starting items: ".length).split(", ").map { it.toLong() }.toMutableList(),
            op = lines[2]["  Operation: new = old ".length],
            operand = lines[2].substring("  Operation: new = old x ".length).toLongOrNull(),
            testDivisor = lines[3].substring("  Test: divisible by ".length).toLong(),
            trueMonkey = lines[4].substring("    If true: throw to monkey ".length).toInt(),
            falseMonkey = lines[5].substring("    If false: throw to monkey ".length).toInt()
        )
    }

    // AREN'T I A CLEVER MONKEY
    val mod = monkeys.map { it.testDivisor }.product()

    for (round in (1..10000)) {
        for (monkey in monkeys) {
            for (item in monkey.items) {
                monkey.inspects++
                var newVal = item
                when (monkey.op) {
                    '+' -> newVal += (monkey.operand ?: item)
                    '*' -> newVal *= (monkey.operand ?: item)
                }
                newVal %= mod
                monkeys[
                    if (newVal % monkey.testDivisor == 0L) monkey.trueMonkey else monkey.falseMonkey
                ].items.add(newVal)
            }
            monkey.items.clear()
        }
    }

    println(monkeys.map { it.inspects }.sortedDescending().take(2).product())
}

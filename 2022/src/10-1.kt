import kotlinx.cli.ArgParser
import kotlinx.cli.ArgType
import java.io.File
import java.lang.IllegalArgumentException


open class Day10VM(val instructions: List<Op>) {
    var x = 1
    var cycle = 1

    interface Op {
        fun exec(vm: Day10VM): Sequence<Int>
    }

    class NoOp : Op {
        override fun exec(vm: Day10VM) = sequence {
            yieldAll(vm.doCycle())
        }
    }

    class AddXOp(val operand: Int) : Op {
        override fun exec(vm: Day10VM) = sequence {
            yieldAll(vm.doCycle())
            yieldAll(vm.doCycle())
            vm.x += operand
        }
    }

    open fun doCycle() = sequence {
        if ((cycle - 20) % 40 == 0) yield(cycle * x)
        cycle++
    }

    open fun run() = sequence {
        instructions.forEach { yieldAll(it.exec(this@Day10VM)) }
    }
}

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 10 part 1")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val xs = Day10VM(File(input).readLines().map {
        val parts = it.split(' ')
        when (parts[0]) {
            "noop" -> Day10VM.NoOp()
            "addx" -> Day10VM.AddXOp(parts[1].toInt())
            else -> throw IllegalArgumentException()
        }
    }).run().toList()

    println(xs)
    println(xs.sum())
}

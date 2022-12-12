import kotlinx.cli.ArgParser
import kotlinx.cli.ArgType
import util.toPixels
import java.io.File
import java.lang.IllegalArgumentException

class Day10Part2VM(instructions: List<Op>) : Day10VM(instructions) {
    override fun doCycle() = sequence {
        yield(if ((x-1..x+1).contains((cycle-1) % 40)) 1 else 0)
        cycle++
    }

    override fun run() = sequence {
        instructions.forEach { yieldAll(it.exec(this@Day10Part2VM)) }
    }
}

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 9 part 1")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    println(
        Day10Part2VM(File(input).readLines().map {
            val parts = it.split(' ')
            when (parts[0]) {
                "noop" -> Day10VM.NoOp()
                "addx" -> Day10VM.AddXOp(parts[1].toInt())
                else -> throw IllegalArgumentException()
            }
        }).run().toList().chunked(40).toPixels()
    )
}

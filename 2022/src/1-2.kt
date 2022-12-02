import kotlinx.cli.ArgParser
import kotlinx.cli.ArgType
import java.io.File

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 1 part 2")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val lines = File(input).readLines()

    var elveCalories = mutableListOf<Int>()
    var calories = 0;
    for (line in lines) {
        if (line.isNotBlank()) {
            calories += line.toInt()
        } else {
            elveCalories.add(calories)
            calories = 0
        }
    }

    elveCalories.sortDescending()

    println(elveCalories.slice(0..2).sum())
}
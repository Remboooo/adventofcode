import kotlinx.cli.*
import java.io.File
import kotlin.math.max

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 1 part 1")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    val lines = File(input).readLines()

    var maxCalories = 0;
    var calories = 0;
    for (line in lines) {
        if (line.isNotBlank()) {
            calories += line.toInt()
        } else {
            maxCalories = max(calories, maxCalories)
            calories = 0
        }
    }

    println(maxCalories)
}
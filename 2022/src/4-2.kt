import kotlinx.cli.*
import util.asRangeLongBitmask
import util.toPair
import java.io.File

fun main(args: Array<String>) {
    val parser = ArgParser("AoC day 4 part 2")
    val input by parser.argument(ArgType.String, description = "Input file")
    parser.parse(args)

    println(
        File(input).readLines()
            .map { it.split(',') }
            .map { elf ->
                elf.map {
                    it.split('-').map { s -> s.toInt() }.toPair().asRangeLongBitmask(128)
                }.toPair()
            }.count { (a1, a2) -> a1.hasOverlapWith(a2) }
    )
}

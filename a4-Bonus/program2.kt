import java.io.BufferedReader
import java.io.File
import kotlin.*

fun main() {
    val bufferedReader: BufferedReader = File("example.txt").bufferedReader()
    val inputString = bufferedReader.use { it.readText() }
    println(inputString)
}

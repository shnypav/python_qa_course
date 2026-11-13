fun main() {
    print("What is your name? ")
    System.out.flush()
    val name = readLine() ?: ""
    println("Hello, $name!")
}

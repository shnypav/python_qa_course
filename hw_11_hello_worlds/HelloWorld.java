import java.util.Scanner;

public class HelloWorld {
    public static void main(String[] args) {
        System.err.println("[INFO] Program started");
        Scanner scanner = new Scanner(System.in);
        System.out.print("What is your name? ");
        String name = scanner.nextLine();
        System.out.println("Hello, " + name + "!");
        System.err.println("[INFO] Greeting printed");
    }
}

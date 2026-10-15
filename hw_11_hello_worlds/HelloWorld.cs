using System;

class HelloWorld
{
    static void Main()
    {
        Console.Write("What is your name? ");
        string name = Console.ReadLine() ?? "";
        Console.WriteLine($"Hello, {name}!");
    }
}

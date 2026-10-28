#include <iostream>
#include <string>

int main() {
    std::string name;

    std::cerr << "[INFO] Program started\n";
    std::cout << "What is your name? ";
    std::getline(std::cin, name);
    std::cout << "Hello, " << name << "!\n";

    std::cerr << "[INFO] Greeting printed\n";
    return 0;
}

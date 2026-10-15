package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)

	fmt.Print("What is your name? ")
	name, _ := reader.ReadString('\n')
	fmt.Printf("Hello, %s!\n", strings.TrimSpace(name))
}

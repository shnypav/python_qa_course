import Foundation

print("What is your name? ", terminator: "")
fflush(stdout)
let name = readLine() ?? ""
print("Hello, \(name)!")

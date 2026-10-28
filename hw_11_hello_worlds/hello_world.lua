io.stderr:write("[INFO] Program started\n")
io.write("What is your name? ")
local name = io.read() or ""
print("Hello, " .. name .. "!")
io.stderr:write("[INFO] Greeting printed\n")

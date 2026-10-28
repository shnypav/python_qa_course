puts stderr {[INFO] Program started}
puts -nonewline "What is your name? "
flush stdout
gets stdin name
puts "Hello, $name!"
puts stderr {[INFO] Greeting printed}

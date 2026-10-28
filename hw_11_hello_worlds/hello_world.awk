BEGIN {
    print "[INFO] Program started" > "/dev/stderr"
    printf "What is your name? "
    getline name
    print "Hello, " name "!"
    print "[INFO] Greeting printed" > "/dev/stderr"
}

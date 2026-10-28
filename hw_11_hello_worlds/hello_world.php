<?php

fwrite(STDERR, "[INFO] Program started\n");

echo "What is your name? ";
$name = trim(fgets(STDIN));
echo "Hello, $name!\n";
fwrite(STDERR, "[INFO] Greeting printed\n");

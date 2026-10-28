use strict;
use warnings;

print STDERR "[INFO] Program started\n";
print "What is your name? ";
chomp(my $name = <STDIN>);
print "Hello, $name!\n";
print STDERR "[INFO] Greeting printed\n";

use std::io::{self, Write};

fn main() {
    eprintln!("[INFO] Program started");
    let mut name = String::new();

    print!("What is your name? ");
    io::stdout().flush().unwrap();
    io::stdin().read_line(&mut name).unwrap();

    println!("Hello, {}!", name.trim());
    eprintln!("[INFO] Greeting printed");
}

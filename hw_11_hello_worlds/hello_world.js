console.error("[INFO] Program started");
const readline = require("readline");

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.question("What is your name? ", (name) => {
  console.log(`Hello, ${name}!`);
  console.error("[INFO] Greeting printed");
  rl.close();
});

import logging

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logging.info("Program started")
name = input("What is your name? ")
print(f"Hello, {name}!")
logging.info("Greeting printed")

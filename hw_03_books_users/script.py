import csv
import json
import logging
from datetime import datetime
from pathlib import Path


LOGGER = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR.parent / "logs"


def configure_logging():
    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / f"hw_03_books_users_{datetime.now():%Y%m%d_%H%M%S_%f}.log"
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    console_handler = logging.StreamHandler()
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.propagate = False
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(console_handler)
    LOGGER.info("Writing books/users logs to %s", log_file)
    return file_handler, console_handler


def load_users(path):
    """Load the source users and keep only fields required by the task."""
    try:
        with path.open("r", encoding="utf-8") as file_users:
            users = json.load(file_users)
    except (OSError, json.JSONDecodeError):
        LOGGER.exception("Failed to read users from %s", path)
        raise

    if not isinstance(users, list):
        LOGGER.error("Users source %s must contain a JSON list, got %s", path, type(users).__name__)
        raise ValueError("Users source must contain a JSON list")

    filtered_users = []
    for index, user in enumerate(users):
        if not isinstance(user, dict):
            LOGGER.error("User at index %s is not an object: %r", index, user)
            raise ValueError(f"User at index {index} must be an object")
        filtered_users.append({field: user.get(field) for field in ("name", "gender", "address", "age")})

    LOGGER.info("Loaded and filtered %s users from %s", len(filtered_users), path)
    return filtered_users


def load_books(path):
    """Load all books from the source CSV file."""
    try:
        with path.open("r", encoding="utf-8", newline="") as file_books:
            books = list(csv.DictReader(file_books))
    except (OSError, csv.Error):
        LOGGER.exception("Failed to read books from %s", path)
        raise

    LOGGER.info("Loaded %s books from %s", len(books), path)
    return books


def assign_books(users, books):
    """Distribute books round-robin, preserving the original assignment order."""
    if not users:
        if books:
            LOGGER.error("Cannot assign %s books because there are no users", len(books))
            raise ValueError("Cannot assign books without users")
        return users

    for user in users:
        user["books"] = []

    for book_index, book in enumerate(books):
        user = users[book_index % len(users)]
        user["books"].append(book)
        LOGGER.debug("Assigned book %s to user %s", book.get("Title", book_index), user.get("name"))

    LOGGER.info("Assigned %s books across %s users", len(books), len(users))
    return users


def write_result(path, users):
    try:
        with path.open("w", encoding="utf-8") as result_file:
            json.dump(users, result_file, indent=4, ensure_ascii=False)
    except (OSError, TypeError):
        LOGGER.exception("Failed to write result to %s", path)
        raise
    LOGGER.info("Wrote %s users with books to %s", len(users), path)


def main():
    handlers = configure_logging()
    try:
        users = load_users(BASE_DIR / "users.json")
        books = load_books(BASE_DIR / "books.csv")
        write_result(BASE_DIR / "result.json", assign_books(users, books))
    finally:
        for handler in handlers:
            LOGGER.removeHandler(handler)
            handler.close()


if __name__ == "__main__":
    main()

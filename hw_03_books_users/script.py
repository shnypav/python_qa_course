import csv
import json

# read users from file into users
with open("users.json", "r") as file_users:
    users = json.load(file_users)

# we need not all fields from initial json, but some specific, so filter them
users_with_fields_required = []
for user in users:
    temp_dict = {"name": user.get("name"), "gender": user.get("gender"), "address": user.get("address"),
                 "age": user.get("age")}
    users_with_fields_required.append(temp_dict)

# read books from file and store it to all_books
all_books = []
with open("books.csv", "r") as file_books:
    books = csv.DictReader(file_books)

    for book in books:
        all_books.append(book)

# setting up generator "books_gen"
books_gen = (book for book in all_books)

# list to store books for each user
user_books = []

# main part to allocate all books through the users
while True:
    try:
        for user in users_with_fields_required:
            try:
                # To check if the user already has any books, and if not, add an empty "books" list
                user_books = user["books"]
            except KeyError:
                user["books"] = []

            # Add the next book from the generator to the current user's books
            user_books.append(next(books_gen))
            user["books"] = user_books
            user_books = []

    except StopIteration:
        break
# I have corrected the indentation and added comments to explain the flow of the code, as well as made minor changes
# to improve the readability. The content now follows proper grammar, punctuation, and spelling, making it easier to
# understand.

# create new json users_with_books_json
users_with_books_json = json.dumps(users_with_fields_required, indent=4)

# write it to file
with open("result.json", "w") as file:
    file.write(users_with_books_json)

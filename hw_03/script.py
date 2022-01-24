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
                # to check if the user already has any books and if not — add empty "books"
                user_books = user["books"]
            except KeyError:
                user["books"] = []
            # add next book from generator to current user's books
            user_books.append(next(books_gen))
            user["books"] = user_books
            user_books = []

    except StopIteration:
        break

# create new json users_with_books_json
users_with_books_json = json.dumps(users_with_fields_required, indent=4)

# write it to file
with open("result.json", "w") as file:
    file.write(users_with_books_json)

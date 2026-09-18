from admin import find_book, load_library, save_library


## Search books by category, case-insensitive
def books_in_category(books, category):
    target = category.strip().lower()
    result = []
    for book_id, book in books.items():
        if book["category"].lower() == target:
            result.append(book_id)
    return result


## Search books by full or partial title, case-insensitive
def search_by_title(books, search_text):
    text = search_text.strip().lower()
    result = []
    for book_id, book in books.items():
        if text in book["title"].lower():
            result.append(book_id)
    return result


## Borrow a book
def borrow_book(books, loans, search_text, borrower):
    book_id = find_book(books, search_text)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    name = borrower.strip()
    if name == "":
        return "EMPTY_NAME"

    if not books[book_id]["available"]:
        return "NOT_AVAILABLE"

    books[book_id]["available"] = False
    loans.append({"book_id": book_id, "borrower": name})
    return "OK"


## Return a book
def return_book(books, loans, book_title, borrower):
    book_id = find_book(books, book_title)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    name = borrower.strip()
    if name == "":
        return "EMPTY_NAME"

    if books[book_id]["available"]:
        return "NOT_ON_LOAN"

    books[book_id]["available"] = True
    for i, loan in enumerate(loans):
        if loan["book_id"] == book_id:
            loans.pop(i)
            break
    return "OK"


def main():
    data = load_library("library.json")
    books = data["books"]
    loans = data["loans"]

    while True:
        print("\nLIBRARY USER SYSTEM")
        print("=" * 40)
        print("1. Search by title")
        print("2. Search by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            text = input("Enter title keyword: ")
            ids = search_by_title(books, text)
            if ids:
                print(f"Found {len(ids)} book(s):")
                for bid in ids:
                    print(f"  {bid} - {books[bid]['title']}")
            else:
                print("No books found.")

        elif choice == "2":
            cat = input("Enter category: ")
            ids = books_in_category(books, cat)
            if ids:
                print(f"Found {len(ids)} book(s):")
                for bid in ids:
                    print(f"  {bid} - {books[bid]['title']}")
            else:
                print("No books found.")

        elif choice == "3":
            bid = input("Enter book ID: ")
            borrower = input("Enter your name: ")
            result = borrow_book(books, loans, bid, borrower)
            print(result)

        elif choice == "4":
            bid = input("Enter book ID: ")
            borrower = input("Enter your name: ")
            result = return_book(books, loans, bid, borrower)
            print(result)

        elif choice == "5":
            save_library(data, "library.json")
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()


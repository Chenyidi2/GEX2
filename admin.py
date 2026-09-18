import json


## Load library data from a JSON file
def load_library(filename):
    with open(filename, "r") as f:
        return json.load(f)


## Save library data to a JSON file
def save_library(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


## Find a book by ID, case-insensitive
def find_book(books, search_text):
    cleaned = search_text.strip().lower()
    for book_id in books:
        if book_id.lower() == cleaned:
            return book_id
    return None


## Display all books in the catalogue
def display_books(books):
    print("\nBOOK CATALOGUE")
    print("-" * 60)
    for book_id, book in books.items():
        status = "ON LOAN" if not book["available"] else "AVAILABLE"
        print(f"{book_id} | {book['title']} | {book['category']} | {status}")


## Display all current loans
def display_loans(loans, books):
    print("\nCURRENT LOANS")
    print("-" * 60)
    for loan in loans:
        book_id = loan["book_id"]
        title = books[book_id]["title"] if book_id in books else "Unknown"
        print(f"{book_id} | {title} | Borrower: {loan['borrower']}")


## Calculate library statistics, returns a tuple (total, available, borrowed)
def library_statistics(books):
    total = len(books)
    available = 0
    for book in books.values():
        if book["available"]:
            available += 1
    borrowed = total - available
    return (total, available, borrowed)


def main():
    data = load_library("library.json")
    lib = data["library"]

    print("LIBRARY ADMINISTRATION")
    print("=" * 60)
    print(f"Library: {lib['name']}")
    print(f"Branch: {lib['branch']}")
    print(f"Year: {lib['year']}")
    print(f"Categories: {', '.join(data['categories'])}")

    display_books(data["books"])
    display_loans(data["loans"], data["books"])

    total, avail, borrowed = library_statistics(data["books"])
    print("\nSTATISTICS")
    print("-" * 60)
    print(f"Total books: {total}")
    print(f"Available: {avail}")
    print(f"Borrowed: {borrowed}")


if __name__ == "__main__":
    main()

import weakref
import re

class User():
    def __init__(self, name, email):
        self.name = name
        assert ("@" in email and re.search(".com|.edu|.org", email)), "Invalid e-mail address format."
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        assert ("@" in email and re.search(".com|.edu|.org", email)), "Invalid e-mail address format."
        self.email = address
        print("E-mail address updated.")

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        sum = 0
        num_rated_books = 0
        for book in self.books.keys():
            if self.books[book] != None:
                sum += self.books[book]
                num_rated_books += 1
        return sum / num_rated_books

    def __repr__(self):
        return "User {name}, e-mail: {address}, books read: {num_books}".format(name=self.name, address=self.email, num_books=len(self.books))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

class Book():
    instances = []

    def __init__(self, title, isbn, price):
        assert (isbn not in [instance.isbn for instance in self.__class__.instances]), "A Book object already exists with that ISBN!"
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []
        self.__class__.instances.append(weakref.proxy(self))

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def get_price(self):
        return self.price

    def set_isbn(self, isbn):
        self.isbn = isbn
        print("Updated ISBN for {title}".format(title=self.title))

    def add_rating(self, rating):
        if rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def get_average_rating(self):
        if len(self.ratings) == 0:
            return None
        sum = 0
        for rating in self.ratings:
                sum += rating
        return sum / len(self.ratings)

    def __repr__(self):
        return self.title

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn and self.price == other_book.price

class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)

class TomeRater():
    def __init__(self):
        self.users = {}
        self.books = {}

    def __repr__(self):
        return "Users: \n{users}\n\nBooks: \n{books}".format(users=self.users, books=self.books)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.users == other.users and self.books == other.books
        return False

    def create_book(self, title, isbn, price):
        return Book(title, isbn, price)

    def create_novel(self, title, author, isbn, price):
        return Fiction(title, author, isbn, price)

    def create_non_fiction(self, title, subject, level, isbn, price):
        return Non_Fiction(title, subject, level, isbn, price)

    def add_book_to_user(self, book, email, rating=None):
        if email not in self.users:
            print("No user with e-mail {email}!".format(email=email))
        else:
            self.users[email].read_book(book, rating)
            if rating != None:
                book.add_rating(rating)
            if book in self.books:
                self.books[book] += 1
            else:
                self.books[book] = 1

    def add_user(self, name, email, user_books=None):
        if email in self.users:
            print("Error: That user already exists.")
        else:
            user = User(name, email)
            self.users[email] = user
            if user_books != None:
                for book in user_books:
                    self.add_book_to_user(book, email)

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def get_most_read_book(self):
        return max(self.books, key=lambda key: self.books[key])

    def highest_rated_book(self):
        highest_rated = None
        highest_rating = 0
        for book in self.books.keys():
            rating = book.get_average_rating()
            if rating > highest_rating:
                highest_rated = book                
                highest_rating = rating
        return highest_rated

    def most_positive_user(self):
        positive_user = None
        highest_rating = 0
        for user in self.users.values():
            avg_user_rating = user.get_average_rating()
            if avg_user_rating > highest_rating:
                positive_user = user
                highest_rating = avg_user_rating
        return positive_user

    def get_n_most_read_books(self, n):
        sorted_by_value = sorted(self.books.items(), key=lambda kv: kv[1], reverse=True)
        return sorted_by_value[0:n]

    def get_n_most_prolific_readers(self, n):
        readers = []
        for email in self.users:
            books_read = len(self.users[email].books)
            readers.append((books_read, email))
        readers.sort(reverse=True)

        if n > len(readers):
            n = len(readers)

        result = []
        for i in range(n):
            result.append(self.users[readers[i][1]])
        return result

    def get_n_most_expensive_books(self, n):
        most_expensive_books = []
        for book in self.books.keys():
            most_expensive_books.append((book.price, book))
        most_expensive_books.sort(reverse=True)

        if n > len(most_expensive_books):
            n = len(most_expensive_books)

        return most_expensive_books[0:n]

    def get_worth_of_user(self, user_email):
        total_worth = 0
        user = self.users[user_email]
        
        for book in user.books:
            total_worth += book.price
        return "Total price of books owned by user {0}: ${1:.2f}".format(user_email, total_worth)
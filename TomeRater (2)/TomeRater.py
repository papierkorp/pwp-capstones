class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = dict() #book : rating

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("The Users eMail Address has been updated.")


    def __repr__(self):
        return "Name: {name}, E-Mail: {email}, Books read: {books}\n".format(name=self.name, email=self.email, books=len(self.books))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and self.email == other.email
        return False

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        total_rating = 0
        total_books = len(self.books)
        for rating in self.books.values():
            total_rating += rating
        return total_rating / total_books


class Book:
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = list()

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("The ISBN Number has been updated.")

    def add_rating(self, rating):
        if rating != None:
            if rating in range(0,5):
                self.ratings.append(rating)
            else:
                print("Invalid Rating")

    def __repr__(self):
        return ("Book: {title}, ISBN: {isbn}, Average Rating: {rating}\n".format(title=self.title, isbn=self.isbn, rating= self.get_average_rating()))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.title == other.title and self.isbn == other.isbn
        return False

    def get_average_rating(self):
        total_rating = 0
        total_ratings = len(self.ratings)
        for rating in self.ratings:
            total_rating += rating
        if total_rating == 0:
            return "Not rated yet."
        else:
            return total_rating / total_ratings

    def __hash__(self):
        return hash((self.title, self.isbn))



class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "Title: {}, by {}. ISBN: {}".format(self.title,self.author, self.isbn)


class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{}, a {} manual on {}. ISBN: {}".format(self.title, self.level, self.subject, self.isbn)

class TomeRater:
    def __init__(self):
        self.users = dict() #Users email:User Object
        self.books = dict() #Book Object : Number of Users that read it

    def test_isbn(self, isbn):
        for book in self.books.keys():
            if book.isbn == isbn:
                print("The ISBN Number is already in use.")
                return False
        return True

    def create_book(self, title, isbn):
        if self.test_isbn(isbn):
            new_book = Book(title, isbn)
            self.books[new_book] = 0
            return new_book

    def create_novel(self, title, author, isbn):
        if self.test_isbn(isbn):
            new_novel = Fiction(title, author, isbn)
            self.books[new_novel] = 0
            return new_novel

    def create_non_fiction(self, title, subject, level, isbn):
        if self.test_isbn(isbn):
            new_non_fiction = Non_Fiction(title, subject, level, isbn)
            self.books[new_non_fiction] = 0
            return new_non_fiction

    def add_book_to_user(self, book, email, rating=None):
        if email in self.users:
            Userobj = self.users.get(email)
            Userobj.read_book(book, rating)
            book.add_rating(rating)
            if book not in self.books:
                self.books[book] = 1
            else:
                self.books[book] += 1
        else:
            print("No user with email: {email}!".format(email=email))

    def add_user(self, name, email, books=None):
        if email in self.users:
            print("The user already exists.")
        elif "@" not in email:
            print("No valid email address.")
        else:
            new_User = User(name, email)
            self.users[email] = new_User
        #self.add_book_to_user = [book for book in books if not type(books)] #would this work somehow?
        if books is not None:
            for book in books:
                self.add_book_to_user(book, email)

    def __repr__(self):
        return "Users: {} \nBooks: {}".format(self.users,[book for book in self.books.keys()])

    def print_catalog(self):
        for book in self.books.keys():
            print("{} \n".format(book))

    def print_users(self):
        for user in self.users.values():
            print("{} \n".format(user))

    def most_read_book(self):
        i = 0
        erg = None
        for book in self.books.keys():
            if i < self.books.get(book):
                i = self.books.get(book)
                erg = book
        return "{}, Times Read: {}".format(erg, i)

    def highest_rated_book(self):
        highest_rating = 0
        erg = None
        for book in self.books:
            if highest_rating < book.get_average_rating():
                highest_rating = book.get_average_rating()
                erg = book
        return "{}, Rating: {}".format(erg, highest_rating)

    def most_positive_user(self):
        most_positive = 0
        erg= None
        for user in self.users:
            if most_positive < self.users[user].get_average_rating():
                most_positive = self.users[user].get_average_rating()
                erg = self.users[user]
        return "{}, Rating: {}".format(erg, most_positive)

    def get_n_most_read_books(self, n):
        #book:number of read
        try:
            if type(n) != int:
                return "No Valid number."
            sorted_read_books = sorted(self.books.items(), key=lambda x: x[1], reverse=True)

            for i in range(n):
                print("{}.: {} with {} readers.".format(i+1, sorted_read_books[i][0], sorted_read_books[i][1]))
        except IndexError:
            print("Not enough books in the database.")



    def get_n_most_prolific_readers(self, n):
        #email:user
        try:
            if type(n) != int:
                return "No Valid number."

            new_try = dict()
            for email, user in self.users.items():
                new_try[email] = len(user.books)

            sorted_nt = sorted(new_try.items(), key=lambda x: x[1], reverse=True)

            for i in range(n):
                print("{}.: {}".format(i+1, self.users[sorted_nt[i][0]]))
        except IndexError:
            print("Not enough User in the database.")




x =TomeRater()
Markus = User("Markus", "xxx@ymail.com")
book1 = Book("Book1", 123456789)
book2 = Book("Book2", 456789012)
book3 = Book("Book3", 789012345)
book4 = Book("Book4", 78901234)
book5 = Book("Book5", 7890123)
Markus.read_book(book1, 3)
Markus.read_book(book2, 1)
Markus.read_book(book3, 4)
book1.add_rating(2)
book1.add_rating(1)
book1.add_rating(3)
book1.add_rating(4)
book1.add_rating(2)
book2.add_rating(3)
book2.add_rating(4)
book2.add_rating(2)
book3.add_rating(1)
book3.add_rating(2)
book3.add_rating(3)
x.add_user("Lukas", "xxx@gmx.de", [book1,book2])
x.add_user("Markus", "xxx@ymail.com")
x.add_user("Robert", "xxx@aol.com", [book2])
x.add_user("Jo", "xxx@gmail.com", [book1, book2, book3])
x.add_book_to_user(book1, "xxx@ymail.com", 3)
x.add_book_to_user(book2, "xxx@ymail.com", 2)
x.add_book_to_user(book3, "xxx@ymail.com", 1)
x.add_book_to_user(book4, "xxx@ymail.com", 4)
x.add_book_to_user(book5, "xxx@ymail.com", 4)
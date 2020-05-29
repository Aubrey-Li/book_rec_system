import csv  # https://docs.python.org/3/library/csv.html
import random  # https://docs.python.org/3/library/random.html
from dataclasses import dataclass

with open('books.csv', encoding="utf8") as f:
    lines = list(csv.reader(f))  # loads lines of books.csv into list of lists

with open('genres.txt') as f:
    # loads list of genres.txt to display on main page into list of strings
    # we have this list because otherwise there are too many books to display
    # and the website will get overloaded.
    display_genres = list(map(lambda line: line[0], csv.reader(f, delimiter="\n")))


@dataclass(frozen=True)
class Book:
    # ** do not modify this dataclass **
    title: str
    author: str
    genre: str
    img_url: str
    rating: float  # out of 5 stars
    reviews: int  # number of reviews on amazon
    ident: int  # identifier


id_to_book_dict = {}  # map from ID (integer) to book (Book)
genre_to_books_dict = {}  # map from genre (string) to all books in that genre (list)
book_to_score_dict = {}  # map from book (Book) to its recommendation score (integer)
cart = []
purchases = []


def setup(testing=False):
    """ procedure to setup any global variables (which must be defined
    above this function). """
    if testing:
        return

    id_to_book_dict.clear()
    genre_to_books_dict.clear()
    book_to_score_dict.clear()
    cart.clear()
    purchases.clear()

    ident = 0
    for line in lines:
        rating = line[4]
        reviews = line[5]
        if not rating:
            rating = None
        else:
            rating = float(rating)

        if not reviews:
            reviews = None
        else:
            reviews = int(reviews)

        bk = Book(line[0], line[1], line[2], line[3],
                  rating, reviews, ident)
        id_to_book_dict[ident] = bk
        ident += 1

    for line in lines:
        if line[2] not in display_genres:
            display_genres.append(line[2])

    for bk_num in id_to_book_dict:
        if id_to_book_dict[bk_num].genre not in genre_to_books_dict:
            genre_to_books_dict[id_to_book_dict[bk_num].genre] = [id_to_book_dict[bk_num]]
        else:
            genre_to_books_dict[id_to_book_dict[bk_num].genre].append(id_to_book_dict[bk_num])


# Note: do not change.
def get_cart() -> list:
    """ return current representation of the cart. """
    return cart


def get_book(ident: int) -> Book:
    """ given a book id (integer), return the Book corresponding to that id """
    for bk_num in id_to_book_dict:
        if bk_num == ident:
            update_recs(id_to_book_dict[bk_num])
            return id_to_book_dict[bk_num]


# Note: do not change.
def add_book_to_cart(ident: int):
    """ given the ident of a book, add the corresponding book to th
    cart. no return required. """
    book = get_book(ident)
    if book not in cart:
        cart.append(book)


# Note: do not change.
def remove_book_from_cart(ident: int):
    """ given the ident of a book, remove the corresponding book from
    the cart. no return required """
    book = get_book(ident)
    if book in cart:
        cart.remove(book)


# Note: do not change.
def buy_books_in_cart():
    """ purchase all books in cart. update cart, previous purchases,
    books, recommendations as required. no return required. """
    for book in cart:
        purchases.append(book)
        update_recs(book)
    cart.clear()


# Note: do not change.
def get_purchases() -> list:
    return purchases


# Note: do not change.
def book_matches(query: str, book: Book) -> bool:
    return (query.lower() in book.genre.lower() or
            query.lower() in book.title.lower() or
            query.lower() in book.author.lower())


def search_books(query: str) -> list:
    """ given a query string, return list of matching Books """
    # Updating the recommendations system
    new_words = query.split()
    update_recs_given_query_words(new_words)

    ret = []

    for bk_num in id_to_book_dict:
        if book_matches(query, id_to_book_dict[bk_num]):
            ret.append(id_to_book_dict[bk_num])

    # Sort ret by number of reviews -- do not change
    ret.sort(key=lambda b: 0 if b.reviews is None else b.reviews, reverse=True)
    return ret[:min(50, len(ret))]


def get_book_dict() -> dict:
    """ return a dictionary of genre -> list of books.
    use random.sample to randomly choose some books to display
    for each genre. do not allow the number of books in any given
    genre to be greater than 10. """

    out_dict = {}

    for genre in display_genres:
        out_dict[genre] = random.sample(genre_to_books_dict[genre], 25)
    return out_dict


def get_recommendations() -> list:
    """
    return current recommendations, in order of how recommended the book is
    """
    sorted_list = list(sorted(book_to_score_dict, key=book_to_score_dict.get, reverse=True))
    return sorted_list[:min(50, len(sorted_list))]


def update_recs(book: Book):
    """ given a book, updates the current recommendations
    according to scheme in handout """
    for bk_num in id_to_book_dict:
        BOOK = id_to_book_dict[bk_num]
        if BOOK == book:
            continue

        score = 0
        if BOOK.genre == book.genre:
            score += 1

        if BOOK.author == book.author:
            score += 3

        if score > 0:
            if BOOK in book_to_score_dict:
                book_to_score_dict[BOOK] += score
            else:
                book_to_score_dict[BOOK] = score

    for bk in purchases:
        if bk in book_to_score_dict:
            book_to_score_dict.pop(bk)


def update_recs_given_query_words(queries):
    """ given list of queries (strings), updates the current recommendations
    according to scheme in handout """
    for bk_num in id_to_book_dict:
        BOOK = id_to_book_dict[bk_num]
        score = 0
        for query in queries:
            if book_matches(query, BOOK):
                score += 1

            if score > 0:
                if BOOK in book_to_score_dict:
                    book_to_score_dict[BOOK] += score
                else:
                    book_to_score_dict[BOOK] = score

    for book in purchases:
        if book in book_to_score_dict:
            book_to_score_dict.pop(book)

from testlight import *
from hw10_code import *

# Define all your testing functions here. Use HW9's template for reference.


def test_get_book():
    setup(testing=False)
    test("get Bobby", get_book(0), id_to_book_dict[0])
    test("get davinci", get_book(13), id_to_book_dict[13])


def test_get_rec():
    setup(testing=False)
    search_books("harry potter")
    test("get 50 recs", len(get_recommendations()), 50)
    lst = get_recommendations()
    test("first item has highest score", book_to_score_dict[lst[0]] >= book_to_score_dict[lst[1]], True)


def test_update_rec():
    setup(testing=False)
    get_book(26)
    test("book with same author and genre +4",book_to_score_dict[id_to_book_dict[434]], 4)
    test("similar genre book score +1", book_to_score_dict[id_to_book_dict[0]], 1)
    test("same author different genre book score +3", book_to_score_dict[id_to_book_dict[2862]], 3)

    add_book_to_cart(26)
    test("cumulative score", book_to_score_dict[id_to_book_dict[434]], 8)

    buy_books_in_cart()
    test("book purchased not in rec", id_to_book_dict[26] in book_to_score_dict, False)


def test_search_books():
    setup(testing=False)
    list1 = search_books("tolkien")
    test("find books that has less than 50 matches", len(list1), 27)
    test("empty query 50 results", len(search_books("")), 50)
    test("matching book", search_books("Studio Series Colored Pencil Set (Set of 30)"), [id_to_book_dict[47]])


def test_update_recs_given_query():
    setup(testing=False)
    search_books("tolkien")
    test("books related to tolkien score +1", book_to_score_dict[id_to_book_dict[2155]], 1)
    setup(testing=False)
    search_books("good omens")
    test("rec books w more matching strings score adding up", book_to_score_dict[id_to_book_dict[6447]], 3)


# Written Portion
#   1. Contrasting Dictionary and list, I would recommend using dictionary when dealing with a very large data set, as
# using dictionary can reduce the steps taken to run the code and thus increase running speed. A list would be more
# preferable when I want to present a set of data in order, like the time when the get_recommendations() is implemented.
# If given a choice to choose the code to implement for this large csv file, I would prefer dictionary, as it is more
# direct and it's easier to get access to data corresponding to a key.

#   2. The biggest take aways are--always start thinking about the assignment in blocks and logic chains. It's important
# to know the purpose of the code and what it needs to achieve at first. The next important thing to consider is how to
# divide the assignment into smaller blocks, and how these blocks are connected to one another. Thinking through
# designing these blocks can add clarity and structure to the code and it's also easier to trace back to the code upon
# running into a bug and know what to expect for. Naming functions or variables clearly also helps with understanding
# the code when it gets complicated. If it's possible to simplify code by naming clunky parts beforehand it'd also be
# helpful to understand codes when structure piles up.


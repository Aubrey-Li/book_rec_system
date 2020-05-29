from flask import Flask, redirect, render_template, request, flash, url_for
from hw10_code import get_book, search_books, get_recommendations, get_book_dict, \
                  add_book_to_cart, remove_book_from_cart, buy_books_in_cart, \
                  get_cart, get_purchases, setup

# *** Do not modify this file *** #


app = Flask(__name__)
app.secret_key = '9012uwj1fi3n12i9fj1283fj1208fj1' # no idea what this's for


@app.route("/")
def home():
    return render_template('index.html', books=get_book_dict(),
                           cart=get_cart(), purchased=get_purchases())


@app.route('/view/<book_ident>')
def view(book_ident):
    ident = int(book_ident)
    book = get_book(ident)
    return render_template("view.html", book=book, cart=get_cart(),
                           purchased=get_purchases())


@app.route('/cart')
def show_cart():
    return render_template('cart.html', books=get_cart(), cart=get_cart(),
                           purchased=get_purchases())


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    ident = int(request.form['ident'])
    add_book_to_cart(ident)
    return 'True'


@app.route('/cart_rm/<book_ident>')
def cart_rm(book_ident):
    print("this is the id:" + book_ident)
    remove_book_from_cart(int(book_ident))
    return redirect(url_for('show_cart'))


@app.route('/cart_buy')
def buy():
    buy_books_in_cart()
    flash('Books purchased')
    return redirect('cart')


@app.route("/search", methods=['POST'])
def search():
    query = request.form['query']
    res = search_books(query)  # list of matching books
    if len(res) > 50:
        raise ValueError('search_books returned list with > 50 books')

    return render_template('search.html', books=res, query=query,
                           cart=get_cart(), purchased=get_purchases())


@app.route("/recommendations/")
def recommendations():
    recs = get_recommendations() # sorted list of recs
    if len(recs) > 50:
        raise ValueError('get_recommendations returned list with > 50 books')

    return render_template("recommendations.html", books=recs,
                           cart=get_cart(), purchased=get_purchases())


if __name__ == "__main__":
    setup()
    try:
        app.run(debug=True) # website will show errors when they happen
    except OSError:
        e = 'Cannot run multiple instances of app at same time'
        e += '\nStop all other app.py instances and try again.'
        raise OSError(e)


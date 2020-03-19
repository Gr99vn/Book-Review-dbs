import requests
import csv
from flask import Flask, session, render_template, url_for, redirect, request, flash, jsonify
from sqlalchemy import and_, or_
from db.dbmodels import *

app = Flask(__name__)

env = "prod"
if env == "dev":
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:tran12345@localhost:5432/bookrevser"
else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://fttybtamxebieu:5870020154a31eadf7f5cdfd902924fe40112c523462738332ae47f8797e4c5a@ec2-35-174-88-65.compute-1.amazonaws.com:5432/d4a74cbphmvncr"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.secret_key = b'\x0b`\xd9=9J?\x84\xcc\x10\\\xfe\xb4\xdc\x82\x96'

@app.route("/")
def index():
    if session.get("username") == None :
        return redirect(url_for("login"))
    else:  
        return redirect(url_for("home"))

@app.route("/login", methods=["GET", "POST"])
def login():
    session_username = "NotLogIn"
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        su_email = str(request.form.get("su_email")).lower()
        su_username = str(request.form.get("su_username")).lower()
        su_password = request.form.get("su_password")
        if username != None and password != None:
            if User.query.filter_by(name=username).first() != None:
                _user = User.query.filter_by(name=username).one()
                if password == _user.password:
                    session["username"] = username
                    return redirect(url_for("home"))
                else:
                    flash(u"Password incorrect.", "error")
            else:
                flash(u"User not exist.")
        elif su_email != "" and su_username != "" and str(su_password) != "":
            if User.query.filter_by(name=su_username).first() == None and User.query.filter_by(email=su_email).first() == None:
                user = User(email=su_email, name=su_username, password=su_password)
                db.session.add(user)
                db.session.commit()
                flash("Sign up successfully.")
            else:
                flash(u"Email or username existed.", "error")
            return redirect(url_for("login"))
        else:
            pass
    return render_template("login.html",loginpage=True, session_username=session_username)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route("/home")
def home():
    session_username = str(session.get("username")).capitalize()
    all_book = Book.query.all()
    limit_one_page = 18
    total_page = len(all_book)//limit_one_page +1
    books = []
    b_index = 0
    for book in all_book:
        bkinfo = [b_index, book]
        books.append(bkinfo)
        b_index += 1
    return render_template("home.html", search=True, page_navigate=True, session_username=session_username, total_page=total_page, books=books)

@app.route("/home/search=true", methods=["GET", "POST"])
def home_search():
    session_username = str(session.get("username")).capitalize()
    info = request.form.get('search')
    book_result =[]
    if info != None:
        if str(info).isalnum == True:
            regex = "%" + str(info).strip() + "%"
            book_result = Book.query.filter(or_(Book.isbn.like(regex), Book.year.like(regex))).all()
        else:
            regex = "%" + str(info).strip().title() + "%"
            book_result = Book.query.filter(or_(Book.isbn.like(regex), Book.title.like(regex), Book.author.like(regex))).all()
    if len(book_result) != 0:
        flash(f"Result for search  ' {info} ' :")
        return render_template("home.html", search=True, session_username=session_username, books=book_result, total_page=1)
    else:
        flash(u"No result found!", "error")
        return redirect(url_for("home"))

@app.route("/book/<int:book_id>", methods=["GET", "POST"])
def bookact(book_id):
    session_username = str(session.get("username")).capitalize()

    # Execute submit reviews
    if request.method == "POST" and request.form.get("rating") is not None:
        if session.get("username") != None:
            uname = session.get("username")
            bookId = book_id
            user = User.query.filter_by(name=uname).first()
            checkunique = Review.query.filter(and_(Review.book_id==bookId, Review.user_id==user.id)).first()
            if checkunique == None:
                rating = float(request.form.get("rating")) 
                comment = request.form.get("content")
                newreview = Review(rating=rating, comment=comment, book_id=bookId, user_id=user.id)
                db.session.add(newreview)
                db.session.commit()
                flash("Submmit review successed.")
                return redirect(url_for("bookact", book_id=book_id))
            else:
                flash(u"You had reviewed for this book!", "error")
        else:
            flash(u"Sign in to make a review!", "error")
            return redirect(url_for("login"))
    
    # Get book
    book = Book.query.get(book_id)

    # Get review
    selfreviews =book.review

    # Get ratings_count and average_rating
    self_num_of_rate = len(selfreviews)
    self_avg_rat = 0
    if self_num_of_rate == 0:
        pass
    else:    
        for review in selfreviews:
            self_avg_rat += review.rating
        self_avg_rat /= self_num_of_rate 

    # Get review ratings_count and average_rating from goodread
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "MbLVOZWVjNJs0w6tuTnbIA", "isbns": book.isbn})
    goodreadreviews = res.json()
    num_of_rate = int(goodreadreviews['books'][0]['work_ratings_count'])
    avg_rat = float(goodreadreviews['books'][0]['average_rating'])

    # Get comment
    comments = []
    for rv in selfreviews:
        elem = (rv.comment, str(rv.user.name).capitalize(), int(rv.rating))
        comments.append(elem)
    if len(comments) == 0:
        cmt_available = False
    else:
        cmt_available = True
    return render_template("book.html", session_username=session_username, book=book, self_num_of_rate=self_num_of_rate, self_avg_rat=self_avg_rat, num_of_rate=num_of_rate, avg_rat=avg_rat, comments=comments, cmt_available=cmt_available)

@app.route("/api/<book_isbn>")
def get_api(book_isbn):
    if Book.query.filter_by(isbn=book_isbn).first() == None:
        return jsonify({"error": "ISBN invalid"}), 404
    book = Book.query.filter_by(isbn=book_isbn).one()
    reviews = Review.query.filter_by(book_id=book.id).all()
    review_count = len(reviews)
    average_score = 0
    if review_count == 0:
        pass
    else:    
        for review in reviews:
            average_score += review.rating
        average_score /= review_count 
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": review_count,
        "average_score": average_score
    })

@app.route("/user")
def get_user():
    session_username = str(session.get("username")).capitalize()
    user = User.query.filter_by(name=session.get("username")).one()
    reviews = user.review
    user_reviews = []
    for review in reviews:
        bkt = Book.query.get(review.book_id).title
        info = {
            "book_title": bkt,
            "rating": review.rating,
            "comment": review.comment
        }
        user_reviews.append(info)
    if len(user_reviews) == 0:
        user_reviews = None
    return render_template("user.html", session_username=session_username, user=user, user_reviews=user_reviews)

if __name__ == "__main__":
    app.run()
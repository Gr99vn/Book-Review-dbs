import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dbmodels import *
import csv

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

def main():
  db.create_all()
  f = open("db/books.csv", encoding="utf8")
  reader = csv.reader(f)
  for isbn, title, author, year in reader:
    book = Book(isbn=isbn, title=title, author=author, year=year)
    db.session.add(book)
    print("import", isbn, title, author, year, "success!")
  db.session.commit()  
if __name__ == "__main__":
    with app.app_context():
      main()
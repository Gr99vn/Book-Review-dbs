import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String, nullable=False) 
  name = db.Column(db.String, nullable=False)
  password = db.Column(db.String, nullable=False)
  review = db.relationship("Review", backref="user", lazy=True)

class Book(db.Model):
  __tablename__ = "books"
  id = db.Column(db.Integer, primary_key=True)
  isbn = db.Column(db.String, nullable=False) 
  title = db.Column(db.String, nullable=False) 
  author = db.Column(db.String, nullable=False)
  year = db.Column(db.Integer, nullable=False)
  review = db.relationship("Review", backref="book", lazy=True)

class Review(db.Model):
  __tablename__ = "reviews"
  id = db.Column(db.Integer, primary_key=True)
  rating = db.Column(db.Integer, nullable=False) 
  comment = db.Column(db.Text, nullable=False) 
  book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
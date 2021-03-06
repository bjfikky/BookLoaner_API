import datetime

from peewee import *
from argon2 import PasswordHasher

from config.db import DATABASE
from config.keys import SECRET_KEY


class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE


class Student(Model):
    fullname = CharField()
    passcode = CharField()

    class Meta:
        database = DATABASE


class Book(Model):
    title = CharField()
    author = CharField()
    edition = IntegerField(default=0)
    genre = CharField()

    class Meta:
        database = DATABASE


class Loan(Model):
    student = ForeignKeyField(Student, backref='books_loaned')
    book = ForeignKeyField(Book, backref='loaned_by')
    loan_date = DateTimeField(default=datetime.datetime.now)
    return_date = DateTimeField(null=False)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Student, Book, Loan], safe=True)
    DATABASE.close()





import datetime

from peewee import *
from argon2 import PasswordHasher

DATABASE = MySQLDatabase('BookLoaner', user='root', password='root', host='127.0.0.1', port=8889)

SECRET_KEY = 'GD8794B38BS7793BSISJKJW'


class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE


class Student(Model):
    fullname = CharField()

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
    student = ForeignKeyField(Student, related_name='books_loaned')
    book = ForeignKeyField(Book, related_name='loaned_by')
    loan_date = DateTimeField(default=datetime.datetime.now)
    return_date = DateTimeField()

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Student, Book, Loan], safe=True)
    DATABASE.close()





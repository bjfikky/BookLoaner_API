import json

from flask import Blueprint, jsonify, make_response
from flask_restful import Resource, reqparse, Api, fields, marshal_with, marshal, inputs

import models


book_fields = {
    'title': fields.String,
    'author': fields.String,
    'edition': fields.Integer,
    'genre': fields.String,
    'available': fields.Boolean
}


class BookList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=True,
            help='No book title provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'author',
            required=True,
            help='No book author provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'edition',
            type=inputs.positive,
            help='No book title provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'genre',
            required=True,
            help='No book title provided',
            location=['form', 'json']
        )

        super().__init__()

    def get(self):
        books = []

        for book in models.Book.select():
            books.append(marshal(book, book_fields))
        return {'books': books}

    def post(self):
        args = self.reqparse.parse_args()

        if models.Book.select()\
                .where(models.Book.title == args.get('title') & models.Book.author == args.get('author')).get():
            return make_response(json.dumps({'error': 'A book with the same title and author already exists'}), 409)

        books = models.Book.create(**args)
        return marshal(models.Book.get_by_id(books.id), book_fields)


books_api = Blueprint('resources.books', __name__)
api = Api(books_api)
api.add_resource(
    BookList,
    '/books',
    endpoint='books'
)


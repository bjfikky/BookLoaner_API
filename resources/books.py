from flask import Blueprint, jsonify
from flask_restful import Resource, reqparse, Api, fields, marshal_with, marshal, inputs

import models


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
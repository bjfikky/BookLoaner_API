from flask import Blueprint, jsonify
from flask_restful import Resource, reqparse, Api


class StudentList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'fullname',
            required=True,
            help='No student full name provided',
            location=['form', 'json']
        )

    def get(self):
        return jsonify({'students': [
            {'fullname': 'Benjamin Orimoloye'},
            {'fullname': 'James Doe'},
            {'fullname': 'Jimmy Tillerson'},
        ]
        })


students_api = Blueprint('resources.students', __name__)
api = Api(students_api)

api.add_resource(
    StudentList,
    '/students',
    endpoint='students'
)
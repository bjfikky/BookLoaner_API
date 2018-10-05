from flask import Blueprint, jsonify
from flask_restful import Resource, reqparse, Api, fields, marshal_with

import models


student_fields = {
    'fullname': fields.String
}


class StudentList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'fullname',
            required=True,
            help='No student full name provided',
            location=['form', 'json']
        )

        super().__init__()

    def get(self):
        return jsonify({'students': [
            {'fullname': 'Benjamin Orimoloye'},
            {'fullname': 'James Doe'},
            {'fullname': 'Jimmy Tillerson'},
        ]
        })

    @marshal_with(student_fields)
    def post(self):
        args = self.reqparse.parse_args()
        student = models.Student.create(**args)
        return student.get_by_id(student.id)


students_api = Blueprint('resources.students', __name__)
api = Api(students_api)

api.add_resource(
    StudentList,
    '/students',
    endpoint='students'
)
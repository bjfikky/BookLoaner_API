import json

from flask import Blueprint, jsonify, url_for, make_response
from flask_restful import Resource, reqparse, Api, fields, marshal_with, marshal, abort

import models

book_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.String,
    'edition': fields.Integer,
    'genre': fields.String,
}

student_fields = {
    'id': fields.Integer,
    'fullname': fields.String,
    'passcode': fields.String,
    'loans': fields.List(fields.Nested(book_fields))
}


@marshal_with(book_fields)
def add_loans(student):
    student.loans = []
    for loan in student.books_loaned:

        # check if book has not been returned i.e. return date is empty
        if not loan.return_date:
            book = models.Book.get_by_id(loan.book)
            student.loans.append(book)
    return student.loans


class StudentList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'fullname',
            required=True,
            help='No student full name provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'passcode',
            required=True,
            help='No student passcode provided',
            location=['form', 'json']
        )

        super().__init__()

    def get(self):
        students = []

        for student in models.Student.select():
            student.loans = add_loans(student)
            students.append(marshal(student, student_fields))

        return {'students': students}

    @marshal_with(student_fields)
    def post(self):
        args = self.reqparse.parse_args()
        student = models.Student.create(**args)
        return student.get_by_id(student.id)


class Student(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'fullname',
            required=True,
            help='No student full name provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'passcode',
            required=True,
            help='No student passcode provided',
            location=['form', 'json']
        )

        super().__init__()

    @marshal_with(student_fields)
    def get(self, id):
        try:
            student = models.Student.get_by_id(id)
        except models.DoesNotExist:
            abort(404, message="Student {} does not exist".format(id))
        else:
            return student

    @marshal_with(student_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Student.update(**args).where(models.Student.id == id)
        query.execute()
        return models.Student.get_by_id(id), 200, {'Location': url_for('resources.students.student', id=id)}

    def delete(self, id):
        try:
            models.Student.delete_by_id(id)
        except models.DoesNotExist:
            abort(404, message="Student {} does not exist".format(id))
        else:
            return make_response(json.dumps({'success': 'Student has been successfully deleted'}), 200)


students_api = Blueprint('resources.students', __name__)
api = Api(students_api)

api.add_resource(
    StudentList,
    '/students',
    endpoint='students'
)

api.add_resource(
    Student,
    '/students/<int:id>',
    endpoint='student'
)

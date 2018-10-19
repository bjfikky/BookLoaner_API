import json

from datetime import datetime
import time
from email import utils

from flask import Blueprint, jsonify, url_for, make_response
from flask_restful import Resource, reqparse, Api, fields, marshal_with, marshal, abort

import models


book_fields = {
    'loan_id': fields.Integer,
    'book_id': fields.Integer,
    'title': fields.String,
    'author': fields.String,
    'edition': fields.Integer,
    'genre': fields.String,
    'loan_date': fields.String,
    'return_date': fields.String
}

student_fields = {
    'id': fields.Integer,
    'fullname': fields.String,
    'passcode': fields.String,
    'loans': fields.List(fields.Nested(book_fields))
}


def format_date(date):
    if date:
        return datetime.strptime(date, "%b %d %Y %H:%M:%S")
    return date


@marshal_with(book_fields)
def add_loans(student):
    student.loans = []

    for row in models.Book.select(
            models.Loan.id.alias('loan_id'),
            models.Book.id.alias('book_id'),
            models.Book.title,
            models.Book.author,
            models.Loan.loan_date
    ).join(models.Loan).where(student.id == models.Loan.student).dicts():

        row['loan_date'] = row['loan_date'].strftime("%b %d %Y %H:%M:%S")
        student.loans.append(row)
        # print(row)

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

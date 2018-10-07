from flask import Blueprint, jsonify, url_for
from flask_restful import Resource, reqparse, Api, fields, marshal_with, marshal, abort

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
        students = []

        for student in models.Student.select():
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

        super().__init__()

    @marshal_with(student_fields)
    def get(self, id):
        try:
            student = models.Student.get_by_id(id)
        except models.Student.DoesNotExist:
            abort(404, message="Student {} does not exist".format(id))
        else:
            return student

    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Student.update(**args).where(models.Student.id == id)
        query.execute()
        return models.Student.get_by_id(id), 200, {'Location': url_for('resources.students.student', id=id)}


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

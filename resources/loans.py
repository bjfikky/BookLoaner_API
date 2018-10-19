from flask import Blueprint
from flask_restful import Resource, reqparse, inputs, fields, marshal_with, Api, marshal

import models

loan_fields = {
    'id': fields.Integer,
    'student_id': fields.Integer,
    'book_id': fields.Integer,
    'loan_date': fields.DateTime,
    'return_date': fields.DateTime
}


class LoanList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument(
            'student',
            type=inputs.positive,
            required=True,
            help='No student provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'book',
            type=inputs.positive,
            required=True,
            help='No book provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'return_date',
            type=inputs.datetime,
            location=['form', 'json']
        )

        super().__init__()

    def get(self):
        loans = []

        for loan in models.Loan.select():
            loans.append(marshal(loan, loan_fields))
        return {'loans': loans}

    @marshal_with(loan_fields)
    def post(self):
        args = self.reqparse.parse_args()
        loan = models.Loan.create(**args)
        return models.Loan.get_by_id(loan.id)


class Loan(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument(
            'student',
            type=inputs.positive,
            required=True,
            help='No student provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'book',
            type=inputs.positive,
            required=True,
            help='No book provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'return_date',
            type=inputs.datetime,
            location=['form', 'json']
        )

        super().__init__()


loans_api = Blueprint('resources.loans', __name__)
api = Api(loans_api)

api.add_resource(
    LoanList,
    '/loans',
    endpoint='loans'
)

api.add_resource(
    Loan,
    '/loans/<int:id>',
    endpoint='loan'
)


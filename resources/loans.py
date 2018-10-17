from flask_restful import Resource, reqparse, inputs


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

from flask import Flask
from flask_cors import CORS

import models

from resources.students import students_api
from resources.books import books_api
from resources.loans import loans_api

app = Flask(__name__)
CORS(app)
app.register_blueprint(students_api, url_prefix='/api/v1')
app.register_blueprint(books_api, url_prefix='/api/v1')
app.register_blueprint(loans_api, url_prefix='/api/v1')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    models.initialize()
    app.run(debug=True)

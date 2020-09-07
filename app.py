
import os 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import Result

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/test', methods=['POST'])
def test():
    # Test write to DB
    errors = []
    try:
        result = Result(
            url="http://google.com",
            result_all=0,
            result_no_stop_words=0
        )
        db.session.add(result)
        db.session.flush()
        db.session.refresh(result)
        # result.id
        db.session.commit()
    except Exception as e:
        print(e)
        errors.append("Unable to add item to database.")
        print("Unable to add item to database.")
    return "DONE"

if __name__ == '__main__':
    app.run()
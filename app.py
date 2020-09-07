
import os

from flask import Flask, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os.path import join, dirname, realpath, abspath
# from werkzeug.utils import secure_filename

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'uploads/')
ALLOWED_EXTENSIONS = ['png', 'jpg']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #Max size = 16 MB
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Result

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello():
    return "Welcome to Shrey's Image Repository!"

@app.route('/upload/images', methods=['POST'])
def upload():
    """
        Expected request must have Body->form-data of files (>=1)
    """
    # check if the post request has the files part
    if 'files' not in request.files:
        return {"msg": "No files included in form-data"}, 400

    images = [x for x in request.files.getlist('files') if allowed_file(x.filename)]

    if len(images):
        for img in images:
            filename = img.filename
            #TODO: create uuid names and send back mapping
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {"msg": "Successfully uploaded images.", "tags": "TEST"}, 200
    else:
        return {"msg": "No images received. Make sure they are of types {}".format(ALLOWED_EXTENSIONS)}, 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

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
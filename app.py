
import os
import uuid

from flask import Flask, request, redirect, url_for, send_from_directory, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os.path import join, dirname, realpath, abspath
from werkzeug.utils import secure_filename

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'uploads/')
ALLOWED_EXTENSIONS = ['png', 'jpg']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #Max size = 16 MB
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = 'super secret string'  # Change this!
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Result, User, Image, Permissions

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello():
    return "Welcome to Shrey's Image Repository!"

###################### AUTH ######################

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

@app.route('/user/new', methods = ['POST'])
def new_user():
    """
        Creates new user with username, password combo
    """
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return {"msg": "Missing argument"}, 400
    if User.query.filter_by(username = username).first() is not None:
        return {"msg": "User already exists"}, 400
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return { 'username': user.username }, 201

@app.route('/user/greet')
@auth.login_required
def get_resource():
    return { 'data': 'Hello, %s!' % g.user.username }, 200

###################### AUTH ENDS ######################

###################### IMAGES ######################

@app.route('/upload/images', methods=['POST'])
@auth.login_required
def upload():
    """
        Expected request Body->form-data:
            files (>=1)
            permissions (optional = ['open','public','private]) Default='open'
        Response:
            {
                "msg": "Successfully uploaded images.", 
                "filekeys": {"filename": "filekey", ...}
            }
    """
    # check if the post request has the files part
    print(g.user.username)
    print(g.user.role)

    if 'files' not in request.files:
        return {"msg": "No files included in form-data"}, 400
    print(dir(request))
    if 'permissions' in request.form:
        permits = set(item.value for item in Permissions)
        if request.form.getlist('permissions')[0] not in permits:
            return {"msg": "Permissions not recognized"}, 400
        permission = request.form.getlist('permissions')[0]
    else:
        permission = 'open'

    images = [x for x in request.files.getlist('files') if allowed_file(x.filename)]

    if len(images):
        filemap = {}
        for img in images:
            # create unique keys/names and send back mapping
            old_filename = secure_filename(img.filename)
            ext = old_filename.rsplit('.', 1)[1].lower()
            filekey = str(uuid.uuid4())
            new_filename = "{}.{}".format(filekey, ext)
            filemap[filekey] = old_filename

            # add to sql
            image = Image(
                filekey=filekey, filename=old_filename, ext=ext, username=g.user.username, permissions=permission
            )
            db.session.add(image)

            # save to folder
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        db.session.commit()
        return {"msg": "Successfully uploaded images.", "filekeys": filemap}, 200
    else:
        return {"msg": "No images received. Make sure they are of types {}".format(ALLOWED_EXTENSIONS)}, 400

@app.route('/retrieve/<filekey>')
@auth.login_required
def retrieve_file(filekey):
    #TODO: get specific file based on key
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filekey)

###################### IMAGES ENDS ######################

if __name__ == '__main__':
    app.run()
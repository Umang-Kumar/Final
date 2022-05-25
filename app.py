from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
import os
from flask_socketio import SocketIO

# Configure application
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


try:
    app.config["SECRET_KEY"] = "SECRET_KEY"
    app.config["UPLOAD_FOLDER"] = "static/uploads/"
    app.config["MONGO_DBNAME"] = "gallery"
    app.config["MONGO_URI"] = "mongodb://localhost:27017/gallery"

    mongo = PyMongo(app)
    ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]

except:
    print("ERROR - Can't connect to db")

# Initializing SocketIO
socketio = SocketIO(app, async_mode=None)  # cors_allowed_origins="*"


########################
# welcome
@app.route('/')
def home():
    return render_template('welcome.html')


########################
# dashboard
@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')


########################
@app.route("/gallery/")
def gallery():
    cursor = mongo.db.gallery.find()
    for image in cursor:
        print(image)
    return render_template("gallery.html", gallery=mongo.db.gallery.find())


########################
# Add a new student
@app.route('/addUser/', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        image = request.files["image"]
        description = request.form.get("description")
        facial_description = request.form.get("faceId")
        if image and description and image.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            mongo.db.gallery.insert_one({
                "filename": filename,
                "description": description.strip(),
                "facial_description": facial_description
            })

            flash("Successfully uploaded image to gallery!", "success")
            return redirect(url_for("upload"))
        else:
            flash("An error occurred while uploading the image!", "danger")
            return redirect(url_for("upload"))
    return render_template("upload.html")


########################
# Face-Recognition
@app.route('/video/', methods=['GET'])
def video():
    print("SERVER STARTED")
    return render_template('video.html')


@app.route('/matching/', methods=['GET'])
def matching():
    ls = []
    cursor = mongo.db.gallery.find()
    for image in cursor:
        ls.append([image['description'], image['facial_description']])
        # print(ls)
    return {"data": ls}



@socketio.on('my event', namespace='/video/')
def handle_my_custom_event(json):
    print(str(json))


########################


if __name__ == '__main__':
    socketio.run(app, debug='True')

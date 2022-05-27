import json
import os
import os.path
import pathlib
import shutil
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

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
# Making a labeled folder for face matching
def changes():
    cursor = mongo.db.gallery.find()
    for image in cursor:
        new_dir_name = image["description"]
        new_dir = pathlib.Path('C:/Users/User/PycharmProjects/Final/static/labeled_images/', new_dir_name)
        new_dir.mkdir(parents=True, exist_ok=True)
        old_file_name = image["filename"]
        for root, dirs, files in os.walk('C:/Users/User/PycharmProjects/Final/static/uploads'):
            if old_file_name in files:
                shutil.copy2(f"C:/Users/User/PycharmProjects/Final/static/uploads/{old_file_name}",
                             f'C:/Users/User/PycharmProjects/Final/static/labeled_images/{new_dir_name}/{old_file_name}')
                if os.path.exists(f'C:/Users/User/PycharmProjects/Final/static/labeled_images/{new_dir_name}/1.{old_file_name.split(".")[1]}'):
                    continue
                else:
                    os.rename(f'C:/Users/User/PycharmProjects/Final/static/labeled_images/{new_dir_name}/{old_file_name}',
                              f'C:/Users/User/PycharmProjects/Final/static/labeled_images/{new_dir_name}/1.{old_file_name.split(".")[1]}')
    print("Successful:)")


########################
# Add a new student
@app.route('/addUser/', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        image = request.files["image"]
        description = request.form.get("description")

        if image and description and image.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            mongo.db.gallery.insert_one({
                "filename": filename,
                "description": description.strip(),
                # "facial_description": facial_description
            })

            flash("Successfully uploaded image to gallery!", "success")
            changes()
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


@app.route('/arrayOfFiles/', methods=['GET'])
def array_of_files():
    ls = []
    cursor = mongo.db.gallery.find()
    for image in cursor:
        ls.append({"name": f"{image['description']}"})
    return {"data": ls}



########################


if __name__ == '__main__':
    socketio.run(app, debug='True')

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    g)
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import os.path
import pathlib
import shutil
from datetime import datetime

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

# Configure application
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.before_request
def before_request():
    g.user = None

    if 'username' in session:
        user = params['email']
        g.user = user


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


try:
    app.config["SECRET_KEY"] = "SECRET_KEY"
    app.config["UPLOAD_FOLDER"] = "static/uploads/"
    app.config["SHEET_FOLDER"] = "static/Attendances/"
    app.config["MONGO_DBNAME"] = "gallery"
    app.config["MONGO_URI"] = "mongodb://localhost:27017/gallery"

    mongo = PyMongo(app)
    ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]

except:
    print("ERROR - Can't connect to db")

# Initializing SocketIO
socketio = SocketIO(app, async_mode=None)  # cors_allowed_origins="*"


########################
# login
@app.route("/login/", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        session.pop('username', None)

        login_email = request.form.get("email")
        login_password = request.form.get("password")

        # Ensure username was submitted
        if not login_email:
            return render_template("login.html", messager=1)

        # Ensure password was submitted
        elif not login_password:
            return render_template("login.html", messager=2)

        if login_email == params['email'] and check_password_hash(generate_password_hash(params['password'], method='sha256'), login_password):
            session['username'] = login_email
            return redirect((url_for('dashboard')))

        return render_template("login.html")


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# logout
@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


########################
# welcome
@app.route('/')
def home():
    return render_template('welcome.html')


########################
# dashboard
@app.route('/dashboard/')
def dashboard():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


########################
# A webpage to show all the pupils added
@app.route("/gallery/")
def gallery():
    if not g.user:
        return redirect(url_for('login'))
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
                if os.path.exists(f'C:/Users/User/PycharmProjects/Final/static/labeled_images/{new_dir_name}/1.jpg'):
                    continue
                else:
                    os.rename(
                        f'C:/Users/User/PycharmProjects/Final/static/labeled_images/{new_dir_name}/{old_file_name}',
                        f'C:/Users/User/PycharmProjects/Final/static/labeled_images/{new_dir_name}/1.jpg')
    print("Successful:)")


########################
# Add a new student
@app.route('/addUser/', methods=['GET', 'POST'])
def upload():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == "POST":
        image = request.files["image"]
        description = request.form.get("description")

        if image and description and image.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            mongo.db.gallery.insert_one({
                "filename": filename,
                "description": description.strip(),
            })

            flash("Successfully uploaded image to gallery!", "success")
            changes()
            return redirect(url_for("upload"))
        else:
            flash("An error occurred while uploading the image!", "danger")
            return redirect(url_for("upload"))
    return render_template("upload.html")


########################
# Face-Recognition and then making a csv sheet out of it.
@app.route('/video/', methods=['GET', 'POST'])
def video():
    if not g.user:
        return redirect(url_for('login'))
    print("SERVER STARTED")
    if request.method == 'POST':
        attendance = request.form.get("attendance")
        dict_attendance = json.loads(attendance)
        # cleaning garbage values
        for key in list(dict_attendance):
            if key == "unknown":
                del dict_attendance[key]
        for k, v in dict_attendance.items():
            if v:
                dict_attendance[k] = "Absent"
            else:
                dict_attendance[k] = "Present"
        # Making a file in directory
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        with open(f'{app.config["SHEET_FOLDER"]}/{dt_string} Attendance.csv', 'w') as f:
            for key in dict_attendance.keys():
                f.write("%s,%s\n" % (key, dict_attendance[key]))

        # Also updating the file in database to render later
        mongo.db.sheets.insert_one({
            "filename": f'{dt_string} Attendance.csv'
        })
        return redirect(url_for("dashboard"))
    return render_template('video.html')


# Sending the rollNo and Name to the frontend to get label around faces
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

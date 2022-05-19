from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
import os



# Configure application
app = Flask(__name__)

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

    CORS(app)
except:
    print("ERROR - Can't connect to db")


########################
# index
@app.route('/')
def home():
    return render_template('index.html')


########################
@app.route("/attend/")
def gallery():
    return "Take Attendance!"


########################
# Add a new student
@app.route("/addUser/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        image = request.files["image"]
        description = request.form.get("description")
        if image and description and image.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            mongo.db.gallery.insert_one({
                "filename": filename,
                "description": description.strip()
            })

            flash("Successfully uploaded image to gallery!", "success")
            return redirect(url_for("upload"))
        else:
            flash("An error occurred while uploading the image!", "danger")
            return redirect(url_for("upload"))
    return render_template("upload.html")


if __name__ == '__main__':
    app.run(debug=True)

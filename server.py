import os
from flask import Flask, flash, request, redirect, render_template, session
from werkzeug.utils import secure_filename

from src.routes import *
from src.controllers import AppController

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'zip'}

app = Flask(__name__, template_folder="src/views")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object('config')
# app.add_url_rule("/", view_func=AppController.home_page, methods=['GET', 'POST'])
app.add_url_rule("/preference", view_func=AppController.preference_page, methods=['GET', 'POST'])
app.add_url_rule("/evaluate_metric_layout", view_func=AppController.evaluate_metric_layout, methods=['GET', 'POST'])
# app.add_url_rule("/upload", view_func=AppController.upload_page, methods=['GET', 'POST'])
@app.route("/upload", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            print(request.files['file'])
            return redirect("/progress_bar")
    return render_template("upload.html")
app.add_url_rule("/progress_bar", view_func=AppController.progress_bar_page, methods=['GET', 'POST'])

if __name__ == "__main__":
    from src.models.DB import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)
    app.run(debug=True)

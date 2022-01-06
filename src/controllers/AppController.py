import os
from flask import flash, request, redirect, render_template, session, jsonify
from werkzeug.utils import secure_filename

from .GraphController import run_graph

from .UserController import save_user, get_user_count, get_user_count_having_files
from .SNAController import get_rate
from .FileController import extract_file
import random
from flask import current_app as app
import uuid

ALLOWED_EXTENSIONS = {'zip'}

def upload_page():
    if request.method == "GET":
        if not session.get("current_client_id"):
            ip_address = request.remote_addr
            device_type = request.headers.get("user-agent")
            save_user(ip_address, device_type)
        
        if not session.get("total_user"):
            session["total_user"] = get_user_count()
    
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
            guid = uuid.uuid4().hex
            foldername = secure_filename(guid)
            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], foldername))
            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], foldername, "output"))
            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], foldername, "extract"))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], foldername, "file.zip"))
            session["current_foldername"] = foldername

            return redirect("/preference")
    
    return render_template("upload.html")


def preference_page():
    metric_labels, metrics_rate, metric_ids = get_rate("metric")
    layout_labels, layouts_rate, layout_ids= get_rate("layout")
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(max(len(metric_labels), len(layout_labels)))]
    return render_template("preference.html", colors=colors, layout_data=[layout_labels, layouts_rate, layout_ids], metric_data=[metric_labels, metrics_rate, metric_ids])

def calculate_SNA():
    return True

def evaluate_metric_layout():
    #extract_file('asd123')
    print("im hereeeee")
    if request.method == "POST":
        step = int(request.form["step"])
        print(step)
        if step == 1:
            res = extract_file()
            return jsonify({'data': res})
        if step == 2:
            res = calculate_SNA()
            return jsonify({'data': res})
    metric = request.form['metric']
    layout = request.form['layout']
    print(metric)
    print(layout)
    return redirect('/')

def progress_bar_page(num=0):
    return render_template("progress_bar.html", num=num)


def graph_page():
    fname = session.get("file_name")
    data = run_graph(fname)
    return render_template("graph.html", channels=data)


"""
def home_page():
    
    print(f"Current Client ID: {session.get('current_client_id')}")
    print(f"{get_user_count()}")
    print(f"{get_user_count_having_files()}")

    metric_labels, metrics_rate = get_rate("metric")
    print(metric_labels)
    print(metrics_rate)
    
    layout_labels, layouts_rate = get_rate("layout")
    print(layout_labels)
    print(layouts_rate)
    
    return render_template("app.html")
"""

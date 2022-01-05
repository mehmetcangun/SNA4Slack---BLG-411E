import os
from flask import flash, request, redirect, render_template, session
from werkzeug.utils import secure_filename

from .GraphController import run_graph

from .UserController import save_user, get_user_count, get_user_count_having_files
from .SNAController import get_rate
from .FileController import extract_file
import random
from flask import current_app as app

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
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            print(request.files['file'])
            return redirect("/progress_bar")
    
    return render_template("upload.html")


def preference_page():
    #extract_file('asd123')
    metric_labels, metrics_rate = get_rate("metric")
    layout_labels, layouts_rate = get_rate("layout")
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(max(len(metric_labels), len(layout_labels)))]
    return render_template("preference.html", colors=colors, layout_data=[layout_labels, layouts_rate], metric_data=[metric_labels, metrics_rate])

def evaluate_metric_layout():
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

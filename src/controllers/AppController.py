import os
import random
import uuid

from flask import flash, request, redirect, render_template, session, jsonify
from werkzeug.utils import secure_filename

from .GraphController import run_graph
from .UserController import save_user, get_user_count, get_user_count_having_files
from .SNAController import get_rate, save_sna
from .FileController import extract_file, get_length, save_fileinfo, get_avg_channel_length_in_files, get_avg_user_length_in_files

from flask import current_app as app

ALLOWED_EXTENSIONS = {'zip'}

def upload_page():
    session["total_user"] = get_user_count()
    
    if request.method == "GET":
        if not session.get("current_client_id"):
            ip_address = request.remote_addr
            device_type = request.headers.get("user-agent")
            save_user(ip_address, device_type)
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if not file.filename.endswith("zip"):
            flash('This file extension is not allowed')
            print("Error 1")
            return redirect(request.url)
        
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
            
            session["current_file_size"] = file.content_length
            session["current_foldername"] = foldername

            return redirect("/preference")
    
    return render_template("upload.html")


def preference_page():
    metric_labels, metrics_rate, metric_ids = get_rate("metric")
    layout_labels, layouts_rate, layout_ids= get_rate("layout")
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(max(len(metric_labels), len(layout_labels)))]
    return render_template("preference.html", colors=colors, layout_data=[layout_labels, layouts_rate, layout_ids], metric_data=[metric_labels, metrics_rate, metric_ids])

def calculate_SNA(file_id):
    fname = session.get("current_foldername")
    metric_id = session.get("metric")
    layout_id = session.get("layout")
    
    sna_id = save_sna(layout_id, metric_id, file_id)
    
    data = run_graph(metric_id = metric_id, layout_id = layout_id, foldername=fname)
    if data:
        session["graph_data"] = data
        return True
    return False

def evaluate_metric_layout():
    
    if request.method == "POST":
        step = int(request.form["step"])
        foldername = session["current_foldername"]
        if step == 1:
            res = extract_file()
            
            user_length = get_length(foldername, "users.json")
            channels_length = get_length(foldername, "channels.json")

            file_id = save_fileinfo(session["current_client_id"], str(session["current_file_size"]), channels_length, user_length, session["current_foldername"])

            session["current_file_id"] = file_id

            return jsonify({'data': res})
        
        if step == 2:
            file_id = session.get("current_file_id")
            res = calculate_SNA(file_id)
            return jsonify({'data': res})
        
    return redirect('/')

def progress_bar_page():
    metric = request.form['metric']
    layout = request.form['layout']
    session["metric"] = int(metric)
    session["layout"] = int(layout)
    return render_template("progress_bar.html")

def graph_page():
    data = session.get("graph_data")
    return render_template("graph.html", channels=data)

def statistics_page():
    total_user = get_user_count()
    user_having_files = get_user_count_having_files()
    avg_channel_length_in_files = get_avg_channel_length_in_files()
    avg_user_length_in_files = get_avg_user_length_in_files()
    metric_labels, metrics_rate, metric_ids = get_rate("metric")
    layout_labels, layouts_rate, layout_ids= get_rate("layout")
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(max(len(metric_labels), len(layout_labels)))]
    
    return render_template("statistics.html", colors=colors, layout_data=[layout_labels, layouts_rate, layout_ids], metric_data=[metric_labels, metrics_rate, metric_ids], data={
        "total_user": total_user,
        "user_having_files": user_having_files,
        "avg_channel_length_in_files": avg_channel_length_in_files,
        "avg_user_length_in_files": avg_user_length_in_files,
    })

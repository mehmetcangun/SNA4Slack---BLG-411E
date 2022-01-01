from flask import render_template, request, session, redirect

from .UserController import save_user, get_user_count, get_user_count_having_files
from .SNAController import get_rate

def home_page():
    if request.method == "GET":
        if not session.get("current_client_id"):
            ip_address = request.remote_addr
            device_type = request.headers.get("user-agent")
            save_user(ip_address, device_type)
    
    print(f"Current Client ID: {session.get('current_client_id')}")
    print(f"{get_user_count()}")
    print(f"{get_user_count_having_files()}")

    metrics_rate = get_rate("metric")
    print(metrics_rate)
    
    layouts_rate = get_rate("layout")
    print(layouts_rate)
    
    return render_template("app.html")

def preference_page():
    return render_template("preference.html")

def evaluate_metric_layout():
    metric = request.form['metric']
    layout = request.form['layout']
    print(metric)
    print(layout)
    return redirect('/')

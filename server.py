import os
import time
import shutil
from pytz import utc

from flask import Flask, render_template
from flask_apscheduler import APScheduler

from src.routes import *
from src.controllers import AppController

app = Flask(__name__, template_folder="src/views")

app.config.from_object('config')

app.add_url_rule("/", view_func=AppController.upload_page, methods=['GET', 'POST'])
app.add_url_rule("/preference", view_func=AppController.preference_page, methods=['GET'])
app.add_url_rule("/evaluate_metric_layout", view_func=AppController.evaluate_metric_layout, methods=['GET', 'POST'])
app.add_url_rule("/progress_bar", view_func=AppController.progress_bar_page, methods=['GET', 'POST'])
app.add_url_rule("/graph", view_func=AppController.graph_page, methods=['GET'])
app.add_url_rule("/statistics", view_func=AppController.statistics_page, methods=['GET'])
app.add_url_rule("/update_user_count", view_func=AppController.update_user_count, methods=['GET'])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_no_authorization(e):
  return render_template('403.html'), 403

def trigger_delete_file():
    to_be_deleted = list()    
    for i in os.listdir(app.config['UPLOAD_FOLDER']):
        check_path = os.path.join(app.config['UPLOAD_FOLDER'], i)
        if os.path.isdir(check_path):
            elapsed_time = time.gmtime(time.time() - os.path.getmtime(check_path))
            
            if app.config["DELETE_ELAPSED_STATUS"] == "minutes" and elapsed_time.tm_min >= int(app.config["DELETE_ELAPSED_TIME_VALUE"]):
                to_be_deleted.append(check_path)
            
            if app.config["DELETE_ELAPSED_STATUS"] == "hours" and elapsed_time.tm_ >= int(app.config["DELETE_ELAPSED_TIME_VALUE"]):
                to_be_deleted.append(check_path)

    for i in to_be_deleted:
        shutil.rmtree(i)


if __name__ == "__main__":
    from src.models.DB import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.apscheduler.add_job(
        timezone=utc, 
        func=trigger_delete_file, 
        trigger='interval', 
        minutes=app.config["WAIT_IN_MINUTES"], 
        hours=app.config["WAIT_IN_HOURS"], 
        days=app.config["WAIT_IN_DAYS"],
        id="delete_task")

    app.run()

 

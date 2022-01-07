from flask import Flask, render_template
from src.routes import *
from src.controllers import AppController

app = Flask(__name__, template_folder="src/views")

app.config.from_object('config')

app.add_url_rule("/", view_func=AppController.upload_page, methods=['GET', 'POST'])
app.add_url_rule("/preference", view_func=AppController.preference_page, methods=['GET', 'POST'])
app.add_url_rule("/evaluate_metric_layout", view_func=AppController.evaluate_metric_layout, methods=['GET', 'POST'])
app.add_url_rule("/progress_bar", view_func=AppController.progress_bar_page, methods=['GET', 'POST'])
app.add_url_rule("/graph", view_func=AppController.graph_page, methods=['GET', 'POST'])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_no_authorization(e):
  return render_template('403.html'), 403

if __name__ == "__main__":
    from src.models.DB import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)
    app.run(debug=True)

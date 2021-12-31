from flask import Flask
from src.routes import *

app = Flask(__name__, template_folder="src/views")
app.config.from_object('config')

app.add_url_rule("/", view_func=AppController.home_page)
app.add_url_rule("/preference", view_func=AppController.preference_page)

if __name__ == "__main__":
    app.run()

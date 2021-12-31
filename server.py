<<<<<<< HEAD
from flask import Flask

from src.routes import *
from src.controllers import AppController


app = Flask(__name__, template_folder="src/views")
app.config.from_object('config')
app.add_url_rule("/", view_func=AppController.home_page, methods=['GET', 'POST'])
app.add_url_rule("/preference", view_func=AppController.preference_page)

if __name__ == "__main__":
    from src.models.DB import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)
    app.run()
=======
from flask import Flask
from src.routes import *

app = Flask(__name__, template_folder="src/views")
app.config.from_object('config')

app.add_url_rule("/", view_func=AppController.home_page)


if __name__ == "__main__":
    app.run()
>>>>>>> ad5c79b0a9f3785977c57549d4a36bbec76b3066

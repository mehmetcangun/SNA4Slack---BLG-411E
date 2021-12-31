from flask import render_template


def home_page():
    return render_template("app.html")

def preference_page():
    return render_template("preference.html")

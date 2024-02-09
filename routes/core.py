from flask import Blueprint, render_template

core = Blueprint("core", __name__)


@core.get("/")
def root():
    return render_template("index.html")

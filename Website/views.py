from flask import Blueprint, render_template, request, flash, redirect, url_for

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/about')
def about():
    return render_template("about.html")


@views.route('/work')
def work():
    return render_template("work.html")


@views.route('/projects')
def projects():
    return render_template("projects.html")

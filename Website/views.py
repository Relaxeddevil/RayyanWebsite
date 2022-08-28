from flask import Blueprint, render_template, request, flash, redirect, url_for
from Amazon import *
import time

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


@views.route('/amazon', methods=['GET', 'POST'])
def amazon():
    if request.method == "POST":
        flash('Searching for your results, please provide a few minutes while I scrape')
        input = request.form.get('search')
        df = create_dataframe(input)
        create_bp(df)
        save_to_excel(df)
        # time.sleep(3)

        return render_template('boxplot.html')

    return render_template("amazon.html")

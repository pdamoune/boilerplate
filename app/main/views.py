from flask import render_template, redirect, url_for, abort
from . import main

from flask_login import current_user


@main.route('/', methods=['GET', 'POST'])
def index():
    # if form.validate_on_submit():
    #     return redirect(url_for('.index'))
    return render_template('index.html')


@main.route('/internal', methods=['GET', 'POST'])
def internal():
    abort(500)

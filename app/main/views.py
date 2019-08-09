from flask import render_template, redirect, url_for, abort
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    # if form.validate_on_submit():
    #     return redirect(url_for('.index'))
    return render_template('index.htm',
                           form=form)


@main.route('/internal', methods=['GET', 'POST'])
def internal():
    abort(500)

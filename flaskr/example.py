from flask_login import login_required
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('example', __name__, url_prefix='/example')

@bp.route('/')
@login_required
def example():    

    return render_template('example/example.html')
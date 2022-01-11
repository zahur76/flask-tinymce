from flask_login import login_required
from flask import (
    Blueprint, flash, g,url_for, redirect, render_template, request, make_response, jsonify
)

from .models import Page

import os

from pathlib import Path

from .forms import addPageForm

from . import Config

from . import db

bp = Blueprint('example', __name__, url_prefix='/example')

@bp.route('/', methods=["GET", "POST"])
@login_required
def example():
    if request.method == "POST":
        form = addPageForm()
        if not form.validate_on_submit():
            return redirect(url_for("example.example"))
        toaddpage = Page(
            slug=form.slug.data,
            content=form.content.data,
            title=form.slug.data)
        db.session.add(toaddpage)
        db.session.commit()
        return redirect(url_for("example.example"))

    all_pages = Page.query.all()

    form = addPageForm()

    context = {
        "pages": all_pages,
        "form": form,
    }

    return render_template('example/example.html', **context)


@bp.route('/imageuploader', methods=['POST'])
@login_required
def imageuploader():
    file = request.files.get('file')
    if file:
        filename = file.filename.lower()
            
        BASE_DIR = Path(__file__).resolve().parent
        path = Config.UPLOAD_FOLDER
        
        img_fullpath = os.path.join(path, filename)
        file.save(img_fullpath)
        return jsonify({'location' : filename})
    # fail, image did not upload
    output = make_response(404)
    output.headers['Error'] = 'Image failed to upload'
    return output
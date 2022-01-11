from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class addPageForm(FlaskForm):
    slug = StringField(
        "name",
        [DataRequired()],
        render_kw={
            "class": "form-control",
            "autocomplete": "off",
            "placeholder": "Reference Name",
        },
    )

    content = TextAreaField(
        "Content",
        [],
        render_kw={
            "class": "form-control",
            "rows": "10",
            "autocomplete": "off",
        },
    )

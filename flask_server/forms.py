from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Optional
from flask_babel import lazy_gettext as _l

class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[Optional()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'meta' not in kwargs:
            kwargs['meta'] = {'csrf': False}
        super(SearchForm, self).__init__(*args, **kwargs)
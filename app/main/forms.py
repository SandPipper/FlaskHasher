from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, ValidationError
from wtforms.validators import Required, Length
from ..models import Vocabulary
import hashlib


class AddWordForm(FlaskForm):
    word = StringField('word', validators=[Length(2, 255,
        message='Your word must be at least 2 characters.')])

    def validate_word(self, field):
        if Vocabulary.query.filter_by(word=field.data.lower()).first():
            raise ValidationError('Word already in your vocabulary')


class GetHashersForm(FlaskForm):
    hashers = SelectField('hashers', validators=[Required()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hashers.choices = [(hasher, hasher) for
                                hasher in hashlib.algorithms_guaranteed]

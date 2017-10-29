from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    vocabulary = db.relationship('Vocabulary', backref='author', lazy='dynamic')
    info = db.relationship('UserInfo', backref='info', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError("password is not readable attribute.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def __repr__(self):
        return "<User {}, {}, {}, {}>".format(self.id, self.username,
                                              self.email, self.confirmed)


class Vocabulary(db.Model):
    __tablename__ = "vocabulary"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String)
    hash_word = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "<Vocabulary {}, {}, {}>".format(self.word, self.hash_word,
                                                    self.author)
class UserInfo(db.Model):
    __tablename__ = "userinfo"
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64))
    cookies = db.Column(db.Text)
    agent = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "<UserInfo {}, {}, {}, {}>".format(self.info, self.ip,
                                                    self.cookies, self.agent)

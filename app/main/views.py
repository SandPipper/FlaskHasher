from flask import render_template, url_for, request, jsonify
import json
from flask_login import login_required, current_user
from . import main
from .forms import AddWordForm, GetHashersForm
from ..models import User, Vocabulary, UserInfo
from app import db
import hashlib


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    words = Vocabulary.query.filter_by(author_id=current_user.id).all()

    addWordForm = AddWordForm()
    getHashersForm = GetHashersForm()

    return render_template('index.html', words=words, addWordForm=addWordForm,
                           getHashersForm=getHashersForm)


@main.route('/getHashes', methods=['POST'])
def getHashes():
    data = {'status': 0, 'message': None}
    words = json.loads(request.form['words'])

    for word in words:
        selected_word = Vocabulary.query.filter_by(word=word,
                                                   author_id=current_user.id
                                                   ).first()

        hash_word = hashlib.new(request.form['algorithm'])
        hash_word.update(word.encode())

        selected_word.hash_word = hash_word.hexdigest()
        db.session.add(selected_word)
        db.session.commit()


    data['status'] = 1
    data['message'] = "OK"
    return jsonify(data)


@main.route('/addWord', methods=['POST'])
def addWord():
    addWordForm = AddWordForm()
    data = {'status': 0, 'message': None}

    if addWordForm.validate_on_submit():
        word = Vocabulary(word=addWordForm.word.data.lower(),
                          author_id=current_user.id)
        db.session.add(word)
        db.session.commit()
        data['status'] = 1
        data['message'] = addWordForm.word.data.lower()
        return jsonify(data)

    data['message'] = addWordForm.word.errors
    return jsonify(data)


@login_required
@main.route('/profile', methods=['GET'])
def profile():

    info = UserInfo.query.get(current_user.id)
    if info:
        info.ip = request.remote_addr
        info.cookies = str(request.cookies)
        info.agent = str(request.user_agent)
    else:
        info = UserInfo(user_id=current_user.id, ip=request.remote_addr,
                    agent=str(request.user_agent), cookies=str(request.cookies))

    db.session.add(info)
    db.session.commit()

    user = User.query.filter_by(id=current_user.id).first()
    hash_words = Vocabulary.query.filter_by(author_id=current_user.id).all()
    return render_template('profile.html', hash_words=hash_words,
                                           user=user)

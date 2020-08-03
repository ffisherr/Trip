from flask import render_template, session, g
from flask import redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_cors import CORS

from app import app, db, loginManager, oid
from app.models import User
from app.forms import LoginForm, RegisterForm


cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/')
def index():
    msg = 'Hello from flask'
    return msg
    # return render_template('index.html')


@app.route('/help')
def help():
    return 'help'


@app.route('/info')
def info():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('auth/registration.html', form=form)


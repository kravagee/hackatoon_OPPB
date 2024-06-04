from flask import Flask, request, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import sqlite3
import secrets


server = Flask(__name__)
bcrypt = Bcrypt(server)
server.config['SECRET_KEY'] = secrets.token_urlsafe(32)
server.config['MAIL_SERVER'] = 'smtp.yandex.ru'
server.config['MAIL_PORT'] = 465
server.config['MAIL_USE_SSL'] = True
server.config['MAIL_USERNAME'] = 'task.tracker.2024@yandex.ru'
server.config['MAIL_PASSWORD'] = 'sbibgayalkjxdyou'
mail = Mail(server)
login_manager = LoginManager(server)
login_manager.login_view = '/'


@login_manager.user_loader
def load_user(id):
    con = sqlite3.connect('project.db')
    cur = con.cursor()
    query = cur.execute(f'''SELECT login, hash_password FROM users WHERE id="{id}"''').fetchone()
    con.close()
    return User(id, query[0], query[1])


class User(UserMixin):
    def __init__(self, id, username, hash_password):
        self.id = id
        self.username = username
        self.hash_password = hash_password

    def get_id(self):
        return self.id


@server.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if list(request.form.values())[0] == '1':
            return redirect(url_for('register'))
        elif list(request.form.values())[0] == '2':
            return redirect(url_for('login'))
    return render_template('index.html')


@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        log = request.form['username']
        password = request.form['password']
        con = sqlite3.connect('project.db')
        cur = con.cursor()
        query = f'''SELECT id, hash_password, is_verified FROM users WHERE login="{log}"'''
        data = cur.execute(query).fetchone()
        if data[2] == 1:
            if data and bcrypt.check_password_hash(data[1], password):
                query = cur.execute(f'''SELECT id, hash_password FROM users WHERE login="{log}"''').fetchone()
                user = User(query[0], log, query[1])
                login_user(user)
                con.commit()
                con.close()
                return redirect(url_for('home', username=log))
            con.commit()
            con.close()
            return render_template('login.html', response='Вы неправильно ввели имя пользователя/пароль')
        return redirect(url_for('verify_email', username=log, response='Вы не подтверили почту.'))
    return render_template('login.html')


@server.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        log = request.form['username']
        password = request.form['password']
        con = sqlite3.connect('project.db')
        cur = con.cursor()
        query = cur.execute(f'''SELECT login FROM users WHERE login="{log}"''').fetchall()
        query_sec = cur.execute(f'''SELECT email FROM users WHERE email="{email}"''').fetchall()
        if len(list(query)) >= 1 or len(list(query_sec)) >= 1:
            con.close()
            return render_template('register.html', response='Пользователь с таким именем '
                                                             'или адресом электронной почты уже существует')
        else:
            token = secrets.token_urlsafe(32)
            """Здесь должна быть логика отправки email"""
            query = f'''INSERT INTO users (login, hash_password, token, is_verified, email) VALUES ("{log}", 
            "{bcrypt.generate_password_hash(password).decode("utf-8")}", "{token}", "{0}", "{email}")'''
            cur.execute(query)
            con.commit()
            con.close()
            return redirect(url_for('verify_email', username=log))
    return render_template('register.html')


server.run()
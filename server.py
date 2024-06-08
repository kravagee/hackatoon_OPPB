from flask import Flask, request, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import sqlite3
import secrets
from config import password
from math3 import MyMath


server = Flask(__name__)
bcrypt = Bcrypt(server)
math = MyMath()
server.config['SECRET_KEY'] = secrets.token_urlsafe(32)
server.config['MAIL_SERVER'] = 'smtp.yandex.ru'
server.config['MAIL_PORT'] = 465
server.config['MAIL_USE_SSL'] = True
server.config['MAIL_USERNAME'] = 'reshai.raduysya@yandex.ru'
server.config['MAIL_PASSWORD'] = password
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
        if not data:
            return render_template('login.html', response='Пользователь не найден')
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
            msg = Message(f'Подтвердите свою почту на сайте Решай и Радуйся! Ваш код : {token}',
                          sender='reshai.raduysya@yandex.ru', recipients=[email])
            mail.send(msg)
            query = f'''INSERT INTO users (login, hash_password, token, is_verified, email) VALUES ("{log}", 
            "{bcrypt.generate_password_hash(password).decode("utf-8")}", "{token}", "{0}", "{email}")'''
            cur.execute(query)
            con.commit()
            con.close()
            return redirect(url_for('verify_email', username=log))
    return render_template('register.html')


@server.route('/verify_email/<username>', methods=['GET', 'POST'])
def verify_email(username, response=''):
    if request.method == 'POST':
        token = request.form['confirmationToken']
        con = sqlite3.connect('project.db')
        cur = con.cursor()
        query = cur.execute(f'''SELECT token FROM users WHERE login="{username}"''').fetchone()
        if query[0] == token:
            cur.execute(f'''UPDATE users SET is_verified = 1 WHERE login="{username}"''')
            query = cur.execute(f'''SELECT id, hash_password FROM users WHERE login="{username}"''').fetchone()
            user = User(query[0], username, query[1])
            login_user(user)
            con.commit()
            con.close()
            return redirect(url_for('home', username=username))
        con.commit()
        con.close()
        return render_template('verify_email.html', response='Вы ввели токен не правильно. Проверьте ещё раз.')
    return render_template('verify_email.html', response=response)


@login_required
@server.route('/home/<username>', methods=['GET', 'POST'])
def home(username):
    if request.method == 'POST':
        value = list(request.form.values())[0]
        if value == '0':
            return redirect(url_for('profile', username=username))
        elif value == '1':
            return redirect(url_for('top', username=username))
        elif value == '2':
            return redirect(url_for('examples', username=username))
        else:
            logout_user()
            return redirect(url_for('index'))
    else:
        return render_template('home.html', username=username)


@server.route('/examples/<username>', methods=["POST", "GET"])
@login_required
def examples(username):
    if request.method == 'POST':
        value = list(request.form.values())[0]
        return redirect(url_for('example',  username=username, nameex=value))
    else:
        return render_template('examples.html')


@server.route('/example/<username>/<nameex>', methods=['POST', 'GET'])
@login_required
def example(username, nameex):
    if nameex == "square":
        return redirect(url_for('solving_example', nameex=nameex, username=username, difficult='square'))
    elif nameex == "line":
        return redirect(url_for('solving_example', username=username, nameex=nameex, difficult='line'))
    else:
        return redirect(url_for('difficult', username=username, nameex=nameex))


@server.route('/top/<username>', methods=['GET', 'POST'])
@login_required
def top(username):
    if request.method == 'POST':
        return redirect(url_for('home', username=username))
    con = sqlite3.connect('project.db')
    cur = con.cursor()
    query = cur.execute(f'''SELECT login, points FROM stats ORDER BY points DESC LIMIT 10''').fetchall()
    return render_template('top_users.html', query=query)


@server.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    if request.method == 'POST':
        if list(request.form.values())[0] == '3':
            return redirect(url_for('home', username=username))
    else:
        con = sqlite3.connect('project.db')
        cur = con.cursor()
        query = cur.execute(f'''SELECT solved_examples, examples, points 
        FROM stats WHERE login="{username}"''').fetchone()
        print(query)
        if not query:
            return render_template('private_office.html', solved_examples='Вы ещё не решали примеры',
                                   points=0, percentage_examples=0, username=username)
        percentage = int(query[0]) / int(query[1])
        return render_template('private_office.html', solved_examples=query[0],
                               points=query[2], percentage_examples=query[0], username=username)


@server.route('/difficult/<username>/<nameex>', methods=['GET', 'POST'])
@login_required
def difficult(username, nameex):
    if request.method == 'POST':
        value = list(request.form.values())[0]
        return redirect(url_for('solving_example', nameex=nameex, username=username, difficult=value))
    else:
        return render_template('difficult.html', username=username)


@server.route('/<nameex>/<difficult>/<username>', methods=['GET', 'POST'])
@login_required
def solving_example(nameex, difficult, username):
    if request.method == 'POST':
        anwser = request.form['solving_examples']
        equation = request.form['example_equation']
        if list(request.form.values())[0] == '3':
            return redirect(url_for('home', username=username))
        response = []
        if nameex == 'square':
            response = math.check_answer_square_x(anwser)
        elif nameex == 'line':
            response = math.check_answer_line_x(anwser)
        elif nameex == 'plus':
            if difficult == 'easy':
                response = math.check_answer_sum_stage_1(anwser)
            elif difficult == 'normal':
                response = math.check_answer_sum_stage_2(anwser)
            else:
                response = math.check_answer_sum_stage_3(anwser)
        elif nameex == 'minus':
            if difficult == 'easy':
                response = math.check_answer_min_stage_1(anwser)
            elif difficult == 'normal':
                response = math.check_answer_min_stage_2(anwser)
            else:
                response = math.check_answer_min_stage_3(anwser)
        elif nameex == 'sub':
            if difficult == 'easy':
                response = math.check_answer_crop_stage_1(anwser)
            elif difficult == 'normal':
                response = math.check_answer_crop_stage_2(anwser)
            else:
                response = math.check_answer_crop_stage_3(anwser)
        elif nameex == 'multiply':
            if difficult == 'easy':
                response = math.check_answer_multiply_stage_1(anwser)
            elif difficult == 'normal':
                response = math.check_answer_multiply_stage_2(anwser)
            else:
                response = math.check_answer_multiply_stage_3(anwser)
        return redirect(url_for('example_stats', username=username, response=response[0], example_equation=equation,
                                point=math.edit_rating(username, response[2])))
    else:
        equation = ''
        if nameex == 'square':
            equation = math.generate_square_x()
        elif nameex == 'line':
            equation = math.generate_line_x()
        elif nameex == 'plus':
            if difficult == 'easy':
                equation = math.generate_sum_stage_1()
            elif difficult == 'normal':
                equation = math.generate_sum_stage_2()
            else:
                equation = math.generate_sum_stage_3()
        elif nameex == 'minus':
            if difficult == 'easy':
                equation = math.generate_min_stage_1()
            elif difficult == 'normal':
                equation = math.generate_min_stage_2()
            else:
                equation = math.generate_min_stage_3()
        elif nameex == 'sub':
            if difficult == 'easy':
                equation = math.generate_crop_stage_1()
            elif difficult == 'normal':
                equation = math.generate_crop_stage_2()
            else:
                equation = math.generate_crop_stage_3()
        elif nameex == 'multiply':
            if difficult == 'easy':
                equation = math.generate_multiply_stage_1()
            elif difficult == 'normal':
                equation = math.generate_multiply_stage_2()
            else:
                equation = math.generate_multiply_stage_3()
        return render_template('solving_examples.html', example_equation=equation)


@server.route('/example_stats/<username>/<response>/<example_equation>/<point>', methods=['GET', 'POST'])
@login_required
def example_stats(username, response, example_equation, point):
    if request.method == 'POST':
        return redirect(url_for('home', username=username))
    else:
        con = sqlite3.connect('project.db')
        cur = con.cursor()
        examples = cur.execute(f'''SELECT examples FROM stats WHERE login="{login}"''').fetchone()
        con.close()
        if not examples:
            examples = 1
        else:
            examples += 1
        if response == 'Верно':
            con = sqlite3.connect('project.db')
            cur = con.cursor()
            solved_examples = cur.execute(f'''SELECT solved_examples FROM stats WHERE login="{login}"''').fetchone()
            if not solved_examples:
                solved_examples = 1
            else:
                solved_examples += 1
            cur.execute(f'''UPDATE stats SET solved_examples={solved_examples} WHERE login="{login}"''')
            con.close()
        else:
            point = 0
        con = sqlite3.connect('project.db')
        cur = con.cursor()
        cur.execute(f'''UPDATE stats SET examples={examples} WHERE login="{login}"''')
        con.commit()
        con.close()
        return render_template('example_stats.html', example_equation=example_equation, points=point, response=response)


server.run()
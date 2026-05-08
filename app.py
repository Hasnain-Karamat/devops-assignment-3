from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User(
            username=username,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:
            session['user'] = username
            return redirect('/dashboard')

    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':

        title = request.form['title']

        task = Task(title=title)

        db.session.add(task)
        db.session.commit()

    tasks = Task.query.all()

    return render_template(
        'dashboard.html',
        tasks=tasks
    )

@app.route('/delete/<int:id>')
def delete(id):

    task = Task.query.get(id)

    db.session.delete(task)
    db.session.commit()

    return redirect('/dashboard')

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
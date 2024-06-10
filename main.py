from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://stepa:07052003@localhost/todo_list_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Task('{self.title}')"


@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    task = Task(title=title)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    task = Task.query.get(index)
    if task is None:
        return redirect(url_for('index'))
    if request.method == 'POST':
        task.title = request.form['title']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)


@app.route('/check/<int:index>')
def check(index):
    task = Task.query.get(index)
    if task is not None:
        task.done = not task.done
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:index>')
def delete(index):
    task = Task.query.get(index)
    if task is not None:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

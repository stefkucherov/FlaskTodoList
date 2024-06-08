from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Временное хранилище задач
todos = [{"task": "Sample Todo", "done": False}]


@app.route('/')
def index():
    return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add():
    task = request.form['todo']
    todos.append({"task": task, "done": False})
    return redirect(url_for('index'))


@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    if index < 0 or index >= len(todos):
        return redirect(url_for('index'))
    todo = todos[index]
    if request.method == 'POST':
        todo['task'] = request.form['todo']
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo, index=index)


@app.route('/check/<int:index>')
def check(index):
    if index >= 0 and index < len(todos):
        todos[index]['done'] = not todos[index]['done']
    return redirect(url_for('index'))


@app.route('/delete/<int:index>')
def delete(index):
    if index >= 0 and index < len(todos):
        del todos[index]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from models import db, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

db.init_app(app)

@app.route('/')
def index():
    from models import Task  # Import inside the function to avoid circular imports
    try:
        # Check if the Task table exists
        db.engine.execute('SELECT 1 FROM "task" LIMIT 1')
    except Exception as e:
        # If the table does not exist, create it
        with app.app_context():
            db.create_all()

    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    from models import Task  # Import inside the function to avoid circular imports
    task_content = request.form['content']
    new_task = Task(content=task_content)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

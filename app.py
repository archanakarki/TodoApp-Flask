from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://archanakarki@localhost:5432/todoapp'

db = SQLAlchemy(app)

#Instantiating migrate
migrate = Migrate(app , db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

# Debugging statement
def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

# This db.create_all() command is not required when flask-migrate is run using flask db init
# db.create_all()

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    #Implementation of try-except-finally pattern for error handling
    try:
        description = request.get_json()['description']
        completed = request.get_json()['completed']
        todo = Todo(description=description, completed = completed)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
        body['completed'] = todo.completed
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)

# Update todo completed checkbox route
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

# DELETE 
@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todos(todo_id):
    try:
        Todo.query.filter_by(id = todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'sucess' : True})
    
@app.route('/')
def index():
    return render_template('index.html', todos=Todo.query.order_by('id').all())




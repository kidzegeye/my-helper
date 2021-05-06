import json
import os

from db import db
from db import User, Student, Tutor, Subject, TutorSession, Messages
from flask import Flask
from flask import request

app = Flask(__name__)
db_filename = "tutors.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def missing_parameter_response(body, keys):
    error_output="Missing parameter(s): "
    for key in keys:
        if body.get(key) is None:
            error_output+="'{}', ".format(key)
    return error_output[:-2]

def success_response(data, code=200):
    return json.dumps({"success":True, "data":data}), code

def failure_response(message, code=404):
    return json.dumps({"success":False, "error":message}), code


@app.route("/api/users/")
def get_users():
    return success_response([u.serialize() for u in User.query.all()])

@app.route("/api/students/")
def get_students():
    return success_response([s.serialize() for s in Student.query.all()])

@app.route("/api/tutors/")
def get_tutors():
    return success_response([t.serialize() for t in Tutor.query.all()])

@app.route("/api/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    n = body.get('name')
    nid = body.get('netid')
    loc = body.get('location')
    new_user = User(name = n, netid = nid, location = loc)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

"""
@app.route("/tasks/")
def get_tasks():
    return success_response([t.serialize() for t in Task.query.all()])

@app.route("/subtasks/")
def get_subtasks():
    return success_response([s.serialize() for s in Subtask.query.all()])

@app.route("/categories/")
def get_categories():
    return success_response([c.serialize() for c in Category.query.all()])

@app.route("/tasks/", methods=["POST"])
def create_task():
    body = json.loads(request.data)
    new_task = Task(description = body.get('description', ''), done = body.get('done', False))
    db.session.add(new_task)
    db.session.commit()
    return success_response(new_task.serialize(), 201)

@app.route("/tasks/<int:task_id>/")
def get_task(task_id):
    task = Task.query.filter_by(id=task_id).first() #first only grabs first row, SQL doesn't know it's signualr row
    if task is None:
        return failure_response('Task not found')
    return success_response(task.serialize)

@app.route("/tasks/<int:task_id>/", methods = ["POST"])
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response('Task not found')
    body = json.loads(request.data)
    task.description = body.get('description', task.description)
    task.done = body.get('done', task.done)
    db.session.commit()
    return success_response(task.serialize())

@app.route("/tasks/<int:task_id>/", methods = ["DELETE"])
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response('Task not found')
    db.session.delete(task)
    db.session.commit()
    return success_response(task.serialize())

@app.route("/tasks/<int:task_id>/subtasks/", methods = ["POST"])
def create_subtask(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response('Task not found')
    body = json.loads(request.data)
    new_subtask = Subtask(
        description = body.get('description', ''),
        done = body.get('done', False),
        task_id = task_id
    )
    db.session.add(new_subtask)
    db.session.commit()
    return success_response(new_subtask.serialize())

@app.route("/tasks/<int:task_id>/category/", methods = ["POST"])
def assign_category(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response('Task not found')
    body = json.loads(request.data)
    description = body.get('description')
    if description is None:
        return failure_response("No description")
    category = Category.query.filter_by(description = description).first()
    if category is None:
        category = Category(
            description = description,
            color = body.get('color', 'purple')
        )
    task.categories.append(category)
    db.session.commit()
    return success_response(task.serialize())


"""

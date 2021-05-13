import json
import os

from db import DB
from db import User, Student, Tutor, Subject, TutorSession, Messages, Invite
from flask import Flask
from flask import request

app = Flask(__name__)
DB_filename = "tutors.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % DB_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

DB.init_app(app)
with app.app_context():
    DB.create_all()
    if(Subject.query.filter_by(name="History").first() is None):
        DB.session.add(Subject(name="History"))
        DB.session.add(Subject(name="Math"))
        DB.session.add(Subject(name="Computer Science"))
        DB.session.add(Subject(name="Physics"))
        DB.session.add(Subject(name="Chemistry"))
        DB.session.commit()

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()


def get_user_by_session_token(session_token):
    return User.query.filter(User.session_token == session_token).first()


def get_user_by_update_token(update_token):
    return User.query.filter(User.update_token == update_token).first()

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


@app.route("/")
@app.route("/api/")
@app.route("/api/users/")
def get_users():
    return success_response([u.serialize() for u in User.query.all()])

@app.route("/api/students/")
def get_students():
    return success_response([s.serialize() for s in Student.query.all()])

@app.route("/api/tutors/")
def get_tutors():
    return success_response([t.serialize() for t in Tutor.query.all()])

@app.route("/api/user/<int:user_id>/")
def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("Given user id is not associated with a user!")
    return success_response(user.serialize())

"""
@app.route("/api/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    if body.get("netid") is None or body.get("name") is None or body.get("location") is None:
        return failure_response(missing_parameter_response(body, ["netid", "name", "location"]))
    n = body.get('name')
    nid = body.get('netid')
    loc = body.get('location')
    new_user = User(name = n, netid = nid, location = loc)
    DB.session.add(new_user)
    DB.session.commit()
    return success_response(new_user.serialize(), 201)
"""

@app.route("/api/user/<int:user_id>/tutor/", methods=["POST"])
def add_tutor_to_user(user_id):
    body = json.loads(request.data)
    if body.get("description") is None:
        return failure_response(missing_parameter_response(body, ["description"]))
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("Given user id is not associated with a user!")
    if user.tutor!=[]:
        return failure_response("Given user already a tutor")
    desc = body.get("description")
    rat = body.get("rating", 0)
    new_tutor=Tutor(user_id = user_id, description = desc, rating= rat)
    user.tutor.append(new_tutor)
    DB.session.add(new_tutor)
    DB.session.commit()
    return success_response(new_tutor.serialize(),201)

@app.route("/api/user/<int:user_id>/student/", methods=["POST"])
def add_student_to_user(user_id):
    body = json.loads(request.data)
    if body.get("description") is None:
        return failure_response(missing_parameter_response(body, ["description"]))
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("Given user id is not associated with a user!")
    if user.student!=[]:
        return failure_response("Given user already a student")
    desc = body.get("description")
    new_student=Student(user_id = user_id, description = desc)
    user.student.append(new_student)
    DB.session.add(new_student)
    DB.session.commit()
    return success_response(new_student.serialize(),201)

@app.route("/api/user/<int:user_id>/subject/", methods=["POST"])
def add_subject_to_user(user_id):
    body = json.loads(request.data)
    if body.get("name") is None: #or body.get("code") is None:
        return failure_response(missing_parameter_response(body, ["name"]))#,"code"]))
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("Given user id is not associated with a user!")
    name = body.get("name")
    #code = body.get("code")
    subject = Subject.query.filter_by(name=name).first()#,code=code).first()
    if subject is None:
        return failure_response("No subject found")
    #Math, Science, English, History, Foreign Languages
    if user.tutor is not None:
        for t in user.tutor:
            t.subjects.append(subject)
    if user.student is not None:
        for s in user.student:
            s.subjects.append(subject)
    DB.session.commit()
    return success_response(subject.serialize())

def get_subject_by_name(nme):
    subject=Subject.query.filter_by(name=nme).first()
    if(subject is None):
        return None
    return subject

@app.route("/api/invite/", methods=["POST"])
def create_invite():
    body = json.loads(request.data)
    if body.get("receiver_id") is None or body.get("subject_id") is None:
        return failure_response(missing_parameter_response(body, ["receiver_id","subject_id"]))
    receiver = User.query.filter_by(id=body.get("receiver_id")).first()
    if receiver is None:
        return failure_response("Receiver not found")

    sender=get_logged_in_data()
    if sender is None or type(sender)!=User:
        return failure_response("Invalid session token")
    if sender.id==receiver.id:
        return failure_response("Can't send invite to yourself")
    if receiver.tutor==[] or sender.student==[]:
        return failure_response("Invalid user data")
    tutor=None
    student=None
    for t in receiver.tutor:
        tutor=t
    for s in sender.student:
        student=s
    new_invite=Invite(receiver_id=tutor.id, sender_id=student.id, subject_id=body.get("subject_id"))
    DB.session.add(new_invite)
    DB.session.commit()
    return success_response(new_invite.serialize())

@app.route("/api/invite/<int:invite_id>/",methods=["POST"])
def accept_invite(invite_id):
    invite = Invite.query.filter_by(id=invite_id).first()
    if invite is None:
        return failure_response("Invite not found")
    if invite.accepted:
        return failure_response("Invite already accepted")
    user=get_logged_in_data()
    if user is None or type(user)!=User:
        return failure_response("Invalid session token")
    new_session = invite.create_session(user)
    if new_session is None:
        return failure_response("Authentification mismatch")
    invite.accepted = True
    DB.session.commit()
    return success_response(new_session.rserialize())

def extract_token(request):
    session_token = request.data.get("session")
    if session_token is None:
        return failure_response("Missing auth header")

    return True, session_token

@app.route("/api/register/", methods=["POST"])
def register_account():
    body = json.loads(request.data)

    if body.get("netid") is None or body.get("name") is None or body.get("location") is None or body.get("email") is None or body.get("password") is None:
        return failure_response(missing_parameter_response(body, ["netid", "name", "location" ,"email", "password"]))
    email = body.get("email")
    password = body.get("password")
    n = body.get('name')
    nid = body.get('netid')
    loc = body.get('location')


    optional_user = get_user_by_email(email)

    if optional_user is not None:
        return failure_response("User already exists")

    user = User(email=email, password=password,name = n, netid = nid, location = loc)

    DB.session.add(user)
    DB.session.commit()

    return success_response(user.serialize(), 201)

@app.route("/api/login/", methods=["POST"])
def login():
    body = json.loads(request.data)
    email = body.get("email")
    password = body.get("password")

    if email is None or password is None:
        return failure_response("Invalid email or password")

    user = get_user_by_email(email)

    success= user is not None and user.verify_password(password)
    if not success:
        return failure_response("Invalid email or password")
    return success_response(user.serialize(), 201)


@app.route("/api/session/", methods=["POST"])
def update_session():
    success, update_token = extract_token(request)

    if not success:
        return update_token

    user = get_user_by_update_token(update_token)

    if user is None:
        return failure_response(f"Invalid update token: {update_token}")

    user.renew_session()
    DB.session.commit()

    return success_response(user.serialize(), 201)



def get_logged_in_data():
    success, session_token = extract_token(request)

    if not success:
        return session_token

    user = get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return None
    return user

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

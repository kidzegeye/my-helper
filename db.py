from flask_sqlalchemy import SQLAlchemy
import datetime
import hashlib
import os
import bcrypt

DB = SQLAlchemy()

def get_subject_by_name(nme):
        subject=Subject.query.filter_by(name=nme).first()
        if(subject is None):
            return None
        return subject
#your classes here
subjects_association = DB.Table(
    'subjects_association',
    DB.Column('subject_id', DB.Integer, DB.ForeignKey('subject.id')),
    DB.Column('student_id', DB.Integer, DB.ForeignKey('student.id')),
    DB.Column('tutor_id', DB.Integer, DB.ForeignKey('tutor.id'))
)


class User(DB.Model):
    __tablename__ = "user"
    id = DB.Column(DB.Integer, primary_key = True)
    name = DB.Column(DB.String, nullable = False)
    netid = DB.Column(DB.String, nullable = False)
    location = DB.Column(DB.String, nullable = False)

    email = DB.Column(DB.String, nullable=False, unique=True)
    password_digest = DB.Column(DB.String, nullable=False)
    session_token = DB.Column(DB.String, nullable=False, unique=True)
    session_expiration = DB.Column(DB.DateTime, nullable=False)
    update_token = DB.Column(DB.String, nullable=False, unique=True)

    student = DB.relationship('Student', back_populates = "user", cascade='delete')
    tutor = DB.relationship('Tutor', back_populates = "user", cascade='delete')
    messages = DB.relationship("Messages", back_populates = "user")


    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.netid = kwargs.get('netid')
        self.location = kwargs.get('location')
        self.email=kwargs.get("email")
        self.password_digest = bcrypt.hashpw(kwargs.get("password").encode("utf8"), bcrypt.gensalt(rounds=13))
        self.renew_session()

    def serialize(self):
        return {
            "id":self.id,
            "netid":self.netid,
            "name":self.name,
            "email":self.email,
            "location":self.location,
            "tutor": [t.rserialize() for t in self.tutor],
            "student": [s.rserialize() for s in self.student],
            "session_token":self.session_token,
            "session_expiration": str(self.session_expiration),
            "update_token": self.update_token,
        }
    def rserialize(self):
        return {
            "id":self.id,
            "netid":self.netid,
            "email":self.email,
            "name":self.name,
            "location":self.location,
            "tutor": [t.rserialize() for t in self.tutor],
            "student": [s.rserialize() for s in self.student],
        }

    def _urlsafe_base_64(self):
        return hashlib.sha1(os.urandom(64)).hexdigest()

    def renew_session(self):
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf8"), self.password_digest)

    def verify_session_token(self, session_token):
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration

    def verify_update_token(self, update_token):
        return update_token == self.update_token



class Tutor(DB.Model):
    __tablename__ = "tutor"
    id = DB.Column(DB.Integer, primary_key = True)
    user = DB.relationship('User', back_populates = "tutor", cascade='delete')
    user_id= DB.Column(DB.Integer, DB.ForeignKey('user.id'),nullable=False)
    subjects = DB.relationship('Subject', secondary = subjects_association, back_populates = 'tutor')
    rating = DB.Column(DB.Integer, nullable= True)
    description= DB.Column(DB.String,nullable=False)
    sessions = DB.relationship("TutorSession", back_populates = "tutor", cascade='delete')
    invites=DB.relationship("Invite",back_populates="receiver", cascade="delete")

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.description = kwargs.get('description')
        self.rating=kwargs.get("rating")

    def serialize(self):
        return{
            "id":self.id,
            "rating":self.rating if (self.rating is not None) else 0,
            "description":self.description,
            "sessions":[a.rserialize() for a in self.sessions],
            "subjects":[s.serialize() for s in self.subjects],
            "user": self.user.rserialize(),
            "invites":[i.serialize() for i in self.invites]
        }
    def rserialize(self):
        return{
            "id":self.id,
            "rating":self.rating if (self.rating is not None) else 0,
            "description":self.description,
            "sessions":[a.rserialize() for a in self.sessions],
            "subjects":[s.serialize() for s in self.subjects],
            "invites":[i.rserialize() for i in self.invites]
        }

class Student(DB.Model):
    __tablename__ = "student"
    id = DB.Column(DB.Integer, primary_key = True)
    user = DB.relationship("User", back_populates = "student", cascade='delete')
    user_id= DB.Column(DB.Integer, DB.ForeignKey('user.id'),nullable=False)
    subjects = DB.relationship("Subject", secondary= subjects_association, back_populates="student")
    description = DB.Column(DB.String, nullable=False)
    sessions = DB.relationship("TutorSession",back_populates = "student", cascade='delete')
    invites=DB.relationship("Invite",back_populates="sender", cascade="delete")

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.description = kwargs.get('description')

    def serialize(self):
        return {
            "id":self.id,
            "description":self.description,
            "sessions":[a.rserialize() for a in self.sessions],
            "subjects":[s.serialize() for s in self.subjects],
            "user": self.user.rserialize()

        }

    def rserialize(self):
        return {
            "id":self.id,
            "description":self.description,
            "sessions":[a.rserialize() for a in self.sessions],
            "subjects":[s.serialize() for s in self.subjects],
        }
    

class Subject(DB.Model):
    __tablename__ = "subject"
    id = DB.Column(DB.Integer, primary_key = True)
    name = DB.Column(DB.String, nullable = False)
    #code = DB.Column(DB.String, nullable = False)
    student = DB.relationship('Student', secondary = subjects_association, back_populates = 'subjects')
    tutor = DB.relationship('Tutor', secondary = subjects_association, back_populates = 'subjects')
    sessions = DB.relationship('TutorSession', back_populates = "subject")
    


    def __init__(self, **kwargs):
        #self.code = kwargs.get('code')
        self.name = kwargs.get('name')

    def serialize(self):
        return {
            "id":self.id,
            #"code":self.code,
            "name":self.name
        }


class TutorSession(DB.Model):
    __tablename__ = "tutor_session"
    id = DB.Column(DB.Integer, primary_key = True)
    student = DB.relationship('Student', back_populates = "sessions")
    student_id= DB.Column(DB.Integer, DB.ForeignKey('student.id'),nullable=False)
    tutor = DB.relationship('Tutor', back_populates = "sessions")
    tutor_id= DB.Column(DB.Integer, DB.ForeignKey('tutor.id'), nullable=False)
    messages = DB.relationship('Messages', back_populates = "session", cascade = 'delete')
    subject = DB.relationship('Subject', back_populates = "sessions")
    subject_id= DB.Column(DB.Integer, DB.ForeignKey('subject.id'),nullable=False)
    timestamp = DB.Column(DB.DateTime,default=datetime.datetime.now())

    def __init__(self, **kwargs):
        self.student_id = kwargs.get('student_id')
        self.tutor_id = kwargs.get('tutor_id')
        self.subject_id=kwargs.get("subject_id")

    def serialize(self):
        return {
            "id":self.id,
            "student":[self.student.serialize()],
            "tutor":[self.tutor.serialize()],
            "subject": [self.subject.serialize()],
            "timestamp": self.timestamp.strftime("%D %T")
        }

    def rserialize(self):
        return {
            "id":self.id,
            "student_id":self.student_id,
            "tutor_id":self.tutor_id,
            "subject": [self.subject.serialize()],
            "timestamp": self.timestamp.strftime("%D %T")
        }

class Messages(DB.Model):
    __tablename__ = "messages"
    id = DB.Column(DB.Integer, primary_key = True)
    message=DB.Column(DB.String, nullable=False)

    session = DB.relationship("TutorSession", back_populates = "messages")
    session_id= DB.Column(DB.Integer, DB.ForeignKey('tutor_session.id'),nullable=False)
    user= DB.relationship("User", back_populates = "messages")
    user_id= DB.Column(DB.Integer, DB.ForeignKey('user.id'),nullable=False)

    def __init__(self, **kwargs):
        self.message = kwargs.get('message')

    def serialize(self):
        return {
            "id":self.id,
            "sender":[self.user.serialze()],
            "session":[self.session.serialize()],
            "message":self.message
        }

class Invite(DB.Model):
    __tablename__ = "invites"
    id=DB.Column(DB.Integer, primary_key=True)
    
    sender_id=DB.Column(DB.Integer,DB.ForeignKey('student.id'),nullable=False)
    sender=DB.relationship("Student", back_populates = "invites")

    
    receiver_id=DB.Column(DB.Integer,DB.ForeignKey('tutor.id'),nullable=False)
    receiver=DB.relationship("Tutor", back_populates = "invites")

    subject = DB.relationship('Subject')
    subject_id= DB.Column(DB.Integer, DB.ForeignKey('subject.id'),nullable=False)
    
    accepted=DB.Column(DB.Boolean, default=False)

    def __init__(self, **kwargs):
        self.sender_id=kwargs.get("sender_id")
        self.receiver_id=kwargs.get("receiver_id")
        self.subject_id=kwargs.get("subject_id")

    def serialize(self):
        return {
            "id":self.id,
            "sender":[self.sender.serialize()],
            "receiver":[self.receiver.rserialize()],
            "subject": [self.subject.serialize()],
            "accepted": self.accepted
        }

    def rserialize(self):
        return {
            "id":self.id,
            "sender_id":self.sender.user_id,
            "receiver_id":self.receiver.user_id,
            "subject": self.subject.name,
            "accepted": self.accepted
        }
    
    def getinvites_serialize(self):
        return {
            "id":self.id,
            "sender":[self.sender.user.rserialize()],
            "receiver":[self.receiver.user.rserialize()],
            "subject": [self.subject.serialize()],
            "accepted": self.accepted
        }

    def create_session(self,receiver):
        if receiver.email!=self.receiver.user.email:
            return None
        tutor = self.receiver
        student = self.sender

        new_session = TutorSession(student_id=student.id,tutor_id=tutor.id,subject_id=self.subject.id)
        DB.session.add(new_session)
        DB.session.commit()
        return new_session


    
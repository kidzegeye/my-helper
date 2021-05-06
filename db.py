from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

#your classes here
subjects_association = db.Table(
    'subjects',
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id')),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('tutor_id', db.Integer, db.ForeignKey('tutor.id'))
)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    netid = db.Column(db.String, nullable = False)
    location = db.Column(db.String, nullable = False)
    student = db.relationship('Student', uselist=False,cascade='delete')
    tutor = db.relationship('Tutor', uselist=False,cascade='delete')
    messages = db.relationship("Messages")

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.netid = kwargs.get('netid')
        self.location = kwargs.get('location')

    def serialize(self):
        return {
            "id":self.id,
            "netid":self.netid,
            "name":self.name,
            "location":self.location,
            "tutor": [self.tutor.serialize() if (self.tutor is not None) else ""],
            "student": [self.student.serialize() if (self.student is not None) else ""]
        }
    #password,phone,email

class Tutor(db.Model):
    __tablename__ = "tutor"
    id = db.Column(db.Integer, primary_key = True)
    user = db.relationship('User', uselist=False,cascade='delete')
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    subjects = db.relationship('Subject', secondary = subjects_association, back_populates = 'tutor')
    rating = db.Column(db.Integer, nullable= True)
    description= db.Column(db.String,nullable=False)
    session = db.relationship("TutorSession",cascade='delete')

    def __init__(self, **kwargs):
        self.description = kwargs.get('description')

    def serialize(self):
        return {
            "id":self.id,
            "rating":self.rating if (self.rating is not None) else 0,
            "description":self.description,
            "sessions":[a.rserialize() for a in self.session],
            "subjects":[s.serialize() for s in self.subjects]
        }

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key = True)
    user = db.relationship("User", uselist=False,cascade='delete')
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    subjects = db.relationship("Subject", secondary= subjects_association, back_populates="student")
    description = db.Column(db.String,nullable=False)
    session = db.relationship("TutorSession",cascade='delete')

    def __init__(self, **kwargs):
        self.code = kwargs.get('code')
        self.name = kwargs.get('name')

    def serialize(self):
        return {
            "id":self.id,
            "description":self.description,
            "sessions":[a.rserialize() for a in self.session],
            "subjects":[s.serialize() for s in self.subjects]
        }

class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    code = db.Column(db.String, nullable = False)
    student = db.relationship('Student', secondary = subjects_association, back_populates = 'subjects')
    student_id= db.Column(db.Integer, db.ForeignKey('student.id'),nullable=False)
    tutor = db.relationship('Tutor', secondary = subjects_association, back_populates = 'subjects')
    tutor_id= db.Column(db.Integer, db.ForeignKey('tutor.id'),nullable=False)


    def __init__(self, **kwargs):
        self.code = kwargs.get('code')
        self.name = kwargs.get('name')

    def serialize(self):
        return {
            "id":self.id,
            "code":self.code,
            "name":self.name
        }


class TutorSession(db.Model):
    __tablename__ = "tutor_session"
    id = db.Column(db.Integer, primary_key = True)
    student = db.relationship('Student', uselist=False)
    student_id= db.Column(db.Integer, db.ForeignKey('student.id'),nullable=False)
    tutor = db.relationship('Tutor', uselist=False,)
    tutor_id= db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    messages = db.relationship('Messages', cascade = 'delete')
    subject = db.relationship('Subject', uselist=False)
    subject_id= db.Column(db.Integer, db.ForeignKey('subject.id'),nullable=False)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

    def serialize(self):
        return {
            "id":self.id,
            "student":[self.student.serialize()],
            "tutor":[self.tutor.serialize()],
            "subject": [self.subject.serialize()],
            "timestamp": self.timestamp
        }

    def rserialize(self):
        return {
            "id":self.id,
            "studentid":[self.student.id],
            "tutorid":[self.tutor.id],
            "subject": [self.subject.serialize()],
            "timestamp": self.timestamp
        }

class Messages(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key = True)
    session = db.relationship("TutorSession",uselist = False)
    session_id= db.Column(db.Integer, db.ForeignKey('tutor_session.id'),nullable=False)
    user= db.relationship("User", uselist=False)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    message=db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.message = kwargs.get('message')

    def serialize(self):
        return {
            "id":self.id,
            "sender":[self.user.serialze()],
            "session":[self.session.serialize()],
            "message":self.message
        }




"""
association_table = db.Table(
    'association',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('instructor_id', db.Integer, db.ForeignKey('instructor.id'))
)

class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    assignments = db.relationship('Assignment', cascade = 'delete')
    students = db.relationship('Student', secondary = association_table, back_populates = 'courses')
    instructors = db.relationship('Instructor', secondary = association_table, back_populates = 'courses')

    def __init__(self, **kwargs):
        self.code = kwargs.get('code')
        self.name = kwargs.get('name')

    def serialize(self):
        return {
            "id":self.id,
            "code":self.code,
            "name":self.name,
            "assignments":[a.serialize() for a in self.assignments],
            "users":[u.rSerialize() for u in (self.students + self.instructors)]
        }

    def rSerialize(self):
        return {
            "id":self.id,
            "code":self.code,
            "name":self.name
        }

    def cSerialize(self):
        return {
            "id":self.id,
            "code":self.code,
            "name":self.name,
            "assignments":[a.serialize() for a in self.assignments],
            "students":[s.rSerialize() for s in self.students],
            "instructors":[i.rSerialize() for i in self.instructors]
        }


class Assignment(db.Model):
    __tablename__ = "assignment"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    due_date = db.Column(db.Integer, nullable = False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.due_date = kwargs.get('due_date')
        self.course_id = kwargs.get('course_id')

    def serialize(self):
        return {
            "id":self.id,
            "title":self.title,
            "due_date":self.due_date
        }


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    netid = db.Column(db.String, nullable = False)
    courses = db.relationship('Course', secondary = association_table, back_populates = 'students')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.netid = kwargs.get('netid')

    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "netid":self.netid,
            "courses":[c.serialize() for c in self.courses]
        }

    def rSerialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "netid":self.netid,
        }

class Instructor(db.Model):
    __tablename__ = "instructor"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    netid = db.Column(db.String, nullable = False)
    courses = db.relationship('Course', secondary = association_table, back_populates = 'instructors')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.netid = kwargs.get('netid')

    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "netid":self.netid,
            "courses":[c.serialize() for c in self.courses]
        }

    def rSerialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "netid":self.netid,
        }
"""

"""

#inherit from db.Model
#model for main information, table for all else
class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable = False)
    done = db.Column(db.Boolean, nullable = False)
    subtasks = db.relationship('Subtask', cascade='delete')
    #in this case reference class name
    #cascade: if you delete task, also delete all of the subtasks as well
    categories = db.relationship('Category', secondary=association_table, back_populates = 'tasks')

    #**kwargs enables dictionary as argument
    def __init__(self, **kwargs):
        self.description = kwargs.get('description')
        self.done = kwargs.get('done')

    def serialize(self):
        return{
            'id': self.id,
            'description':self.description,
            'done':self.done,
            'subtasks':[s.serialize() for s in self.subtasks],
            'categories':[c.serialize() for c in self.categories]
        }

class Subtask(db.Model):
    __tablename__ = 'subtask'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable = False)
    done = db.Column(db.Boolean, nullable = False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    def __init__(self, **kwargs):
        self.description = kwargs.get('description')
        self.done = kwargs.get('done')
        self.task_id = kwargs.get('task_id')

    def serialize(self):
        return{
            'id':self.id,
            'description':self.description,
            'done':self.done
        }

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String, nullable = False)
    color = db.Column(db.String, nullable= False)
    tasks = db.relationship('Task', secondary = association_table, back_populates = 'categories')

    def __init__(self, **kwargs):
        self.description = kwargs.get('description')
        self.color = kwargs.get('color')

    def serialize(self):
        return{
            'id':self.id,
            'description':self.description,
            'color':self.color

        }
"""

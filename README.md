# My Helper 
Enabling Cornell students to learn from their peers.

## Link to Android Github Repo:
https://github.com/KennyLiang2302/MyHelper.git

## App Description:
My Helper enables users to sign up as tutors or students. Students can see a list of available tutors and send requests to tutors for a tutoring
session. In turn, tutors can see a list of request for tutoring sessions and accept the tutoring sessions that they would like
to partake in. Our app provides a simple way to allow Cornell students to learn from their surrounding community.

When the user first enters the app, they can choose to login if they have a pre-existing account:  

![Screenshot (13)](https://user-images.githubusercontent.com/83737905/118168365-c77ab800-b3f5-11eb-83ae-e79e94760016.png)
  
Or they can register to make a new account:

![Screenshot (14)](https://user-images.githubusercontent.com/83737905/118168606-090b6300-b3f6-11eb-924e-50ca2b4398a8.png)

If registering to make a new account, they are also prompted to specify if they are a tutor/student and add a short
description:  

![Screenshot (15)](https://user-images.githubusercontent.com/83737905/118168778-36f0a780-b3f6-11eb-9529-943654bd5572.png)

Then, they are prompted to specify what subjects they are interested in teaching/learning:  

![Screenshot (16)](https://user-images.githubusercontent.com/83737905/118168856-4e2f9500-b3f6-11eb-81b4-3d50e6de7561.png)

Upon finishing registration or logging in to a pre-existing account, users that signed up as students will see a list of available
tutors:  

![Screenshot (17)](https://user-images.githubusercontent.com/83737905/118169044-7fa86080-b3f6-11eb-9857-c1883397f6f1.png)

Users that signed up as tutors will see a list of upcoming tutoring session:  

![Screenshot (18)](https://user-images.githubusercontent.com/83737905/118169157-9fd81f80-b3f6-11eb-9ec5-12476564ea08.png)


## Backend Requirements:
We have 7 different tables along with 1 association table. The majority of these tables have relations
with one another, including one-to-one, one-to-many, and many-to-many. Moreover, we have 11 different
working routes and have sent our code to a heroku server.

Heroku Server: https://my-helper-appdev.herokuapp.com/

## API Specification:  
  
### Tables:  
The tables in our database include User, Student, Tutor, Subject, TutorSession, Messages, and Invite.
Moreover, there is an association table called subjects association.

### Routes: 
#### Heroku Server:
Heroku Server: https://my-helper-appdev.herokuapp.com/

#### GET methods:  
  
##### Get all users:  
###### /api/users/
```
{
   "success": <route success>,
   "data": [list of all users]
}
```
  
###### User data (provided for reference):  
```
{
   "id": <user id>,
   "netid": <user netid>,
   "name": <user name>,
   "email": <user email>,
   "location": <user location>,
   "tutor": [if user corresponds to a tutor, list containing one tutor],
   "student": [if user corresponds to a student, list containing one student],
   "session_token": <session token>,
   "session_expiration": <session expiration>,
   "update_token": <session expiration>
}
```
  
##### Get all tutors:  
###### /api/tutors/
```
{
   "success": <route success>,
   "data": [list of tutors]
}
```
 
###### Tutor data (provided for reference):  
```
{
     "id": <tutor id>,
     "rating": <tutor integer rating>,
     "description": <tutor description>,
     "sessions": [list of tutor sessions],
     "subjects": [list of tutor subjects],
     "user": <user corresponding to tutor>,
     "invites": [list of invites for tutoring session]
}
```
  
##### Get all students:  
###### /api/students/  
```
{
   "success": <route success>,
   "data": [list of students]
}
```
  
###### Student data (provided for reference):  
```
{
     "id": <student id>,
     "description": <description of student>,
     "sessions": [list of tutoring sessions],
     "subjects": [list of subjects student wants tutoring in],
     "user": <corresponding user to student>
     "invites_sent": [invites to tutoring sessions student has sent]
}
```
  
##### Get user with user id:  
###### /api/user/<int:user_id>/  
```
{
   "success": <route success>,
   "data": {
       "id": <user id>,
       "netid": <user netid>,
       "name": <user name>,
       "email": <user email>,
       "location": <user location>,
       "tutor": [if user corresponds to a tutor, list containing one tutor],
       "student": [if user corresponds to a student, list containing one student],
       "session_token": <session token>,
       "session_expiration": <session expiration>,
       "update_token": <session expiration>
   }
}
```

##### Get invites with user id:  
###### /api/user/invites/<int:user_id>/
```
{
   "success": <route success>,
   "data": [{
       "id": <invite id>,
       "sender": <sender's user rserialized data>
       "receiver": <receiver's user rserialized data>
       "subject_id": <subject id>
       "accepted": <boolean>
   },..]
}
```
  
#### POST Methods:  
  
##### Register a user:  
###### /api/register/. 
###### Body:  
```
{
   "email":<user email>,
   "password":<user password>,
   "name":<user name>,
   "netid":<user netid>,
   "location":<user location>
}
```
###### Return:  
```
{
   "success": <route success>,
   "data": {
       "id": <user id>,
       "netid": <user netid>,
       "name": <user name>,
       "email": <user email>,
       "location": <user location>,
       "tutor": [if user corresponds to a tutor, list containing one tutor],
       "student": [if user corresponds to a student, list containing one student],
       "session_token": <session token>,
       "session_expiration": <session expiration>,
       "update_token": <session expiration>
   }
}
```
  
##### Login to account:  
###### /api/login/  
###### Body:  
```
{
   "email":<reigstered email>,
   "password":<registered password>
}
```
###### Return:  
```
{
   "success": <route success>,
   "data": {
       "id": <user id>,
       "netid": <user netid>,
       "name": <user name>,
       "email": <user email>,
       "location": <user location>,
       "tutor": [if user corresponds to a tutor, list containing one tutor],
       "student": [if user corresponds to a student, list containing one student],
       "session_token": <session token>,
       "session_expiration": <session expiration>,
       "update_token": <session expiration>
   }
}
```
  
##### Make user a student:  
###### /api/user/<int:user_id>/student/. 
###### Body:
```
{
   "description":<student description>
}
```
###### Return:  
```
{
    "success":<route success>,
    "data":{
       "id": <student id>,
       "description": <description of student>,
       "sessions": [list of tutoring sessions],
       "subjects": [list of subjects student wants tutoring in],
       "user": <corresponding user to student>
       "invites_sent": [invites to tutoring sessions student has sent]
    }
}
```
  
##### Make user a tutor:  
###### /api/user/<int:user_id>/tutor/  
###### Body:  
```
{
   "rating":<tutor rating>,
   "description":<tutor description>
}
```
###### Return:  
```
{
    "success":<route success>,
    "data":{
       "id": <tutor id>,
       "rating": <tutor integer rating>,
       "description": <tutor description>,
       "sessions": [list of tutor sessions],
       "subjects": [list of tutor subjects],
       "user": <user corresponding to tutor>,
       "invites": [list of invites for tutoring session]
    }
}  
```

##### Give user a subject:  
###### /api/user/<int:user_id>/subject/  
###### Body:  
```
{
   "name":<name of subject>
}
```
###### Return:  
```
{
   "success": <route success>,
   "data": {
       "id": <subject id>,
       "name": <subject name>
   }
}
```

##### Send an invite to a tutoring session:  
###### /api/invite/  
###### Body:  
```
{
   "receiver_id":<user id of receiver>,
   "subject_id":<subject to receive tutoring in>,
   "session":<token of user>
}
```
###### Return:  
```
{
     "success": <route success>,
      "data":{
            "id":<invite id>,
            "sender":[list containing the user sender],
            "receiver":[list containing the user receiver],
            "subject": [list containing the subject],
            "accepted": <whether the invite has been accepted>
     }
}
```
  
##### Accept an invite to a tutoring session:  
###### /api/invite/<int:invite_id>/
###### Body:  
```
{
   "session":[list containing tutor_session data]
}
```
###### Return:
```
{
    "success": <route success>,
    "data":{
          "id":<tutor_session id>,
          "student_id":<student id>,
          "tutor_id":<tutor id>,
          "subject_id": <subject_id>,
    }
}
```
     

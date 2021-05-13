# my-helper 
Enabling Cornell students to learn and be tutored by their peers.

## Link to Android Github Repo:
https://github.com/KennyLiang2302/MyHelper.git

## App Description:

## API Specification:  
  
### Tables:  
The tables in our database include User, Student, Tutor, Subject, TutorSession, Messages, and Invite.
Moreover, there is an association table called subjects association.

### Routes:  
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
   "subject_id":<subject to receive tutoring in>
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
            "subject": [list containign the subject],
            "accepted": <whether the invite has been accepted>
     }
}
```
  
##### Accept an invite to a tutoring session:  
###### /api/invite/<int:invite_id>/
###### Return:  
```
{
    "success": <route success>,
    "data":{
          "id":<tutor_session id>,
          "student_id":<student id>,
          "tutor_id":<tutor id>,
          "subject": [subject for tutor session],
          "timestamp": <session time>
    }
}
```
     

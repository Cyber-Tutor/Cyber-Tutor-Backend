import pyrebase
import os

class Firebase:
    def __init__(self):
        self.firebase_config = {
            "apiKey": os.environ['FIREBASE_API_KEY'],
            "authDomain": os.environ['FIREBASE_AUTH_DOMAIN'],
            "databaseURL": os.environ['FIREBASE_DATABASE_URL'],
            "projectId": os.environ['FIREBASE_PROJECT_ID'],
            "storageBucket": os.environ['FIREBASE_STORAGE_BUCKET'],
            "messagingSenderId": os.environ['FIREBASE_MESSAGING_SENDER_ID'],
            "appId": os.environ['FIREBASE_APP_ID'],
        }

        self.firebase = pyrebase.initialize_app(self.firebase_config)
        self.db = self.firebase.database()

    # get user group (experimental or control)
    # TODO: implement user group
    def user_group(self, user_id):
        group = self.db.child("users").child(user_id).child("group").get()
        return group
    
    # returns all quiz questions in given section/chapter/group
    def get_quiz_questions(self, section, chapter, group):
        questions = self.db.child("topics").child(section).child(chapter).child("quiz").child(group).get().val()
        return questions
    
    # returns all test questions in given section/chapter/group
    def get_test_questions(self, section, chapter, group):
        questions = self.db.child("topics").child(section).child(chapter).child("test").child(group).get().val()
        return questions
    
    # gets reading content for given section/chapter/group
    def get_reading(self, section, chapter, group):
        reading = self.db.child("topics").child(section).child(chapter).child(group).get().val()
        return reading['chapterContent']
    

import pyrebase
import dotenv
import os

dotenv.load_dotenv()


"""
Firebase class to interact with Firebase database
"""
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
        group = self.db.child("users").child(user_id).child("group").get().val()
        return group
    
    # returns all quiz questions in given section/chapter/group
    def get_quiz_questions(self, section, chapter, group):
        question_ids = self.db.child("topics").child(section).child(chapter).child("quiz").child(group).get().val()
        questions = []
        for question_id in question_ids:
            question = self.db.child("questions").child("quiz").child(question_id).get().val()
            questions.append(question)
        return questions
    
    # returns all test questions in given section/chapter/group
    def get_test_questions(self, section, group):
        question_ids = self.db.child("topics").child(section).child("test").child(group).get().val()
        questions = []
        for question_id in question_ids:
            question = self.db.child("questions").child("test").child(question_id).get().val()
            questions.append(question)
        return questions
    
    # gets reading content for given section/chapter/group
    def get_reading(self, section, chapter, group):
        reading = self.db.child("topics").child(section).child(chapter).child(group).get().val()
        return reading['chapterContent']
    
    # check answer to quiz question
    # TODO: implement quiz pool
    def check_quiz_answer(self, question_id, answer):
        question = self.db.child("questions").child("quiz").child(question_id).get().val()
        return question['answer'] == answer
    
    # save quiz results
    # TODO: implement user scores
    def save_quiz_score(self, user_id, section, chapter, score):
        self.db.child("users").child(user_id).child("scores").child("quiz").child(section).child(chapter).set({
            "score": score,
        })

    # check answer to test question
    def check_test_answer(self, question_id, answer):
        question = self.db.child("questions").child("test").child(question_id).get().val()
        return question['answer'] == answer
    
    # save test results
    def save_test_score(self, user_id, section, score):
        self.db.child("users").child(user_id).child("scores").child("test").child(section).set({
            "score": score,
        })
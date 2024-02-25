import pyrebase
import dotenv
import os

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

dotenv.load_dotenv()


"""
Firebase class to interact with Firebase database
"""
class Firebase:
    def __init__(self):
        """
        self.firebase_config = {
            "apiKey": os.environ['FIREBASE_API_KEY'],
            "authDomain": os.environ['FIREBASE_AUTH_DOMAIN'],
            "databaseURL": os.environ['FIREBASE_DATABASE_URL'],
            "projectId": os.environ['FIREBASE_PROJECT_ID'],
            "storageBucket": os.environ['FIREBASE_STORAGE_BUCKET'],
            "messagingSenderId": os.environ['FIREBASE_MESSAGING_SENDER_ID'],
            "appId": os.environ['FIREBASE_APP_ID'],
        }
        """
        self.cred = credentials.Certificate(os.environ['FIREBASE_CRED_PATH'])
        self.app = firebase_admin.initialize_app()
        self.db = firestore.client()

        """
        self.firebase = pyrebase.initialize_app(self.firebase_config)
        self.db = self.firebase.database()
        """

    # get user group (experimental or control)
    # TODO: implement user group
    def user_group(self, user_id):
        group = self.db.child("users").child(user_id).child("group").get().val()
        return group
    
    # returns all quiz questions in given section/chapter/group
    def get_quiz_questions(self, section, chapter, group):
        questions_ref = self.db.collection('quizQuestions').document(section).collection(group).document(chapter).collection('questions')
        questions = questions_ref.get()
        return questions
        """
        question_ids = self.db.child("topics").child(section).child(chapter).child("quiz").child(group).get().val()
        questions = []
        for question_id in question_ids:
            question = self.db.child("questions").child("quiz").child(question_id).get().val()
            questions.append(question)
        return questions
        """
    
    # returns all test questions in given section/chapter/group
    def get_test_questions(self, section, group):
        questions_ref = self.db.collection('testQuestions').document(section).collection(group)
        questions = questions_ref.get()
        return questions
        """
        question_ids = self.db.child("topics").child(section).child("test").child(group).get().val()
        questions = []
        for question_id in question_ids:
            question = self.db.child("questions").child("test").child(question_id).get().val()
            questions.append(question)
        return questions
        """
    
    # gets reading content for given section/chapter/group
    def get_reading(self, section, chapter, group):
        reading_ref = self.db.collection('topics').document(section).collection('chapters').document(chapter)
        reading = reading_ref.get()
        content = {
            "title": reading['chapterTitle'],
            "description": reading['chapterDescription'],
            "type": reading['chapterType']
        }
        if group == 'experimentalGroup':
            content['content'] = reading['experimentalGroupContent']
            content['images'] = reading['experimentaalGroupImageURLs']
            return content
        else:
            content['content'] = reading['controlGroupContent']
            content['images'] = reading['controlGroupImageURLs']
            return content
        """
        reading = self.db.child("topics").child(section).child(chapter).child(group).get().val()
        return reading['chapterContent']
        """
    
    # check answer to quiz question
    # TODO: implement quiz pool
    def check_quiz_answer(self, section, chapter, group, question_id, answer):
        question_ref = self.db.collection('quizQuestions').document(section).collection(group).document(chapter).collection('questions').document(question_id)
        question = question_ref.get()
        return question['correctAnswer'] == answer
        """
        question = self.db.child("questions").child("quiz").child(question_id).get().val()
        return question['answer'] == answer
        """
    
    # save quiz results
    # TODO: implement user scores
    def save_quiz_score(self, user_id, section, chapter, score):
        self.db.child("users").child(user_id).child("scores").child("quiz").child(section).child(chapter).set({
            "score": score,
        })

    # check answer to test question
    def check_test_answer(self, section, group, question_id, answer):
        question_ref = self.db.collection('testQuestions').document(section).collection(group).document(question_id)
        question = question_ref.get()
        return question['correctAnswer'] == answer
        """
        question = self.db.child("questions").child("test").child(question_id).get().val()
        return question['answer'] == answer
        """
    # save test results
    def save_test_score(self, user_id, section, score):
        self.db.child("users").child(user_id).child("scores").child("test").child(section).set({
            "score": score,
        })

    # create question in database
    def create_question(self, section, chapter, question):
        self.db.child("questions").child("quiz").set(question)
        self.db.child("topics").child(section).child(chapter).child("quiz").push(question['id'])
        return True
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
        self.cred = credentials.Certificate(os.environ['FIREBASE_CRED_PATH'])
        self.app = firebase_admin.initialize_app()
        self.db = firestore.client()
    
    """
    get user group (experimental or control)
    TODO: implement user group
    """
    def user_group(self, user_id):
        group = self.db.child("users").child(user_id).child("group").get().val()
        return group
    
    """
    returns all quiz questions in given section/chapter/group
    """
    def get_quiz_questions(self, section, chapter, group):
        questions_ref = self.db.collection('quizQuestions').document(section).collection(group).document(chapter).collection('questions')
        questions = questions_ref.get()
        return questions
    
    """
    returns all test questions in given section/chapter/group
    """
    def get_test_questions(self, section, group):
        questions_ref = self.db.collection('testQuestions').document(section).collection(group)
        questions = questions_ref.get()
        return questions
    
    """
    gets reading content for given section/chapter/group
    """
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
        else:
            content['content'] = reading['controlGroupContent']
            content['images'] = reading['controlGroupImageURLs']
        
        return content

    """
    check answer to quiz question
    TODO: implement quiz pool
    """
    def check_quiz_answer(self, section, chapter, group, question_id, answer):
        question_ref = self.db.collection('quizQuestions').document(section).collection(group).document(chapter).collection('questions').document(question_id)
        question = question_ref.get()
        return question['correctAnswer'] == answer

    """
    save quiz results
    TODO: implement user scores
    TODO: redo for new db structure
    """
    def save_quiz_score(self, user_id, section, chapter, score):
        self.db.child("users").child(user_id).child("scores").child("quiz").child(section).child(chapter).set({
            "score": score,
        })

    """
    check answer to test question
    """
    def check_test_answer(self, section, group, question_id, answer):
        question_ref = self.db.collection('testQuestions').document(section).collection(group).document(question_id)
        question = question_ref.get()
        return question['correctAnswer'] == answer

    """
    save test results
    TODO: redo for new db structure
    """
    def save_test_score(self, user_id, section, score):
        self.db.child("users").child(user_id).child("scores").child("test").child(section).set({
            "score": score,
        })

    """
    create question in database
    question is from db_data QuizQuestion
    """
    def create_question(self, section, chapter, question, group):
        question_ref = self.db.collection('quizQuestions').document(section).collection(group).document(chapter).collection('questions')
        all_questions = question_ref.get()
        question_id = len(all_questions) + 1
        question_ref.document(question_id).set(question)
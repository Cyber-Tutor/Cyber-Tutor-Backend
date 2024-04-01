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
        self.app = firebase_admin.initialize_app(self.cred, {
            'projectId': os.environ['FIREBASE_PROJECT_ID'],
        })
        self.db = firestore.client()
    
    """
    Create a new question
    question arg is question in json format of db structure
    """
    def create_question(self, question):
        question_ref = self.db.collection('quizQuestions').document()
        question_ref.set(question)

    """
    Update/add reading content for given section/chapter, group, and difficulty
    """
    def create_reading(self, section, chapter, group, content, difficulty):
        reading_group = f"{group}GroupContent"
        reading_ref = self.db.collection('topics').document(section).collection('chapters').document(chapter)
        # get all chapter content
        chapter_content = reading_ref.get()
        # get reading content for group
        reading = chapter_content.to_dict()[reading_group]
        # add reading content for difficulty
        reading[difficulty] = content
        # update reading content
        reading_ref.update({
            reading_group: reading
        })
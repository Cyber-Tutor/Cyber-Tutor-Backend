from firebase import Firebase
from db_data import QuizQuestion
import json

"""
Reads saved quiz questions from json file and stores them in the database
"""
def save_questions(questions, section, chapter, q_path):
    db = Firebase()

    questions = read_questions(q_path)

    for question in questions:
        quiz_question = {
            'question': question['question']['question'],
            'answer': question['question']['answer'],
            'difficulty': question['difficulty'],
            'choices': question['question']['choices'],
            'explanation': question['question']['explanation'],
            'topics': question['question']['topics'],
            'topicId': section,
            'chapterId': chapter
        }
        db.create_question(quiz_question)


def read_questions(question_path):
    with open(question_path, 'r') as f:
        return json.load(f)
    

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--section', type=int, help='an integer for the section', required=True)
    parser.add_argument('--chapter', type=int, help='an integer for the chapter', required=True)
    parser.add_argument('--path', type=str, help='a string for the quiz json path', required=True)

    args = parser.parse_args()
    save_questions(args.path, args.section, args.chapter, args.path)
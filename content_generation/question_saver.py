from firebase import Firebase
import json

"""
Reads saved quiz questions from json file and stores them in the database
"""
def save_question(section, chapter, quiz_question):
    db = Firebase()
    db.create_question(section, chapter, quiz_question)


def read_questions(question_path):
    with open(question_path, 'r') as f:
        return json.load(f)
    

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--section', type=int, help='an integer for the section')
    parser.add_argument('--chapter', type=int, help='an integer for the chapter')
    parser.add_argument('--question_path', type=str, help='a string for the question path')

    args = parser.parse_args()

    questions = read_questions(args.question_path)
    for question in questions:
        save_question(args.section, args.chapter, question)
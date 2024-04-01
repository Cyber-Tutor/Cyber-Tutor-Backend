from firebase import Firebase
# from db_data import QuizQuestion
import json
import argparse

"""
Reads saved quiz questions from json file and stores them in the database
"""
def save_questions(questions, section, chapter):
    db = Firebase()

    for question in questions:
        quiz_question = {
            'question': question['question'],
            'answer': question['answer'],
            'difficulty': question['difficulty'],
            'choices': question['choices'],
            'explanation': question['explanation'],
            'topicId': section,
            'chapterId': chapter
        }
        db.create_question(quiz_question)


def read_questions(question_path):
    with open(question_path, 'r') as f:
        return json.load(f)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--section', type=str, help='content section', required=True)
    parser.add_argument('--chapter', type=str, help='content chapter', required=True)
    parser.add_argument('--path', type=str, help='a string for the quiz json path', required=True)

    args = parser.parse_args()
    questions = read_questions(args.path)
    save_questions(args.section, args.chapter, args.path)
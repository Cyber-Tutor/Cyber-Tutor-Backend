from question_generator import QuestionGenerator
from firebase import Firebase

import argparse


def quiz_creator(section, chapter, details_path, difficulty, topic):
    if not topic:
        topic = section

    db = Firebase()
    q_gen = QuestionGenerator()
    # get list of question details from file
    details = get_details(details_path)

    # create questions for each detail based on topic, difficulty
    for detail in details:
        question = q_gen.create_question(topic, detail, difficulty)
        quiz_question = {
            "question": question,
            "difficulty": difficulty,
        }
        db.create_question(section, chapter, quiz_question)

def get_details(details_path):
    with open(details_path, 'r') as f:
        return f.readlines()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--section', type=int, help='an integer for the section')
    parser.add_argument('--chapter', type=int, help='an integer for the chapter')
    parser.add_argument('--details_path', type=str, help='a string for the question topics path')
    parser.add_argument('--difficulty', type=str, help='a string for the difficulty')
    parser.add_argument('--topic', type=str, help='a string for the topic')

    args = parser.parse_args()

    quiz_creator(args.section, args.chapter, args.details_path, args.difficulty)

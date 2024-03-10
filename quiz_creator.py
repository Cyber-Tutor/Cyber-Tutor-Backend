from question_generator import QuestionGenerator
#from firebase import Firebase
import json

import argparse


def quiz_creator(details_path, difficulty, topic, q_per_detail=1):
    #db = Firebase()
    q_gen = QuestionGenerator()
    # get list of question details from file
    details = get_details(details_path)
    quiz = []

    # create questions for each detail based on topic, difficulty
    for level in difficulty:
        for detail in details:
            for _ in range(q_per_detail):
                # pass if question generation fails
                question = q_gen.create_question(topic, detail, level)
                if question is None:
                    continue
                
                # test to see if llm output is valid json 
                try: 
                    json.loads(question)
                except json.JSONDecodeError:
                    continue

                quiz_question = {
                    "question": json.loads(question),
                    "difficulty": level,
                }
                #db.create_question(section, chapter, quiz_question)
                quiz.append(quiz_question)

    return quiz

def get_details(details_path):
    with open(details_path, 'r') as f:
        return f.readlines()

def save_quiz(quiz, save_path):
    with open(save_path, 'w') as f:
        json.dump(quiz, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--section', type=int, help='an integer for the section')
    parser.add_argument('--chapter', type=int, help='an integer for the chapter')
    parser.add_argument('--details_path', type=str, help='a string for the question topics path')
    parser.add_argument('--difficulty', nargs='+', help='a list of strings for the difficulty levels', default=['beginner', 'intermediate', 'hard'])
    parser.add_argument('--topic', type=str, help='a string for the topic')
    parser.add_argument('--q_per_detail', type=int, help='an integer for the number of questions to generate per detail', default=1)
    parser.add_argument('--save_path', type=str, help='a string for the save path')

    args = parser.parse_args()

    quiz = quiz_creator(args.details_path, args.difficulty, args.topic, args.q_per_detail)
    save_quiz(quiz, args.save_path)
from question_generator import QuestionGenerator
from question_saver import save_questions

import argparse
import json
import os


def quiz_creator(q_gen, details, difficulty, topic, q_per_detail=1):
    # get list of question details from file
    quiz = []

    # create questions for each detail based on topic, difficulty
    for level in difficulty:
        for detail in details:
            for _ in range(q_per_detail):
                # pass if question generation fails
                question = q_gen.create_question(topic, detail, level)
                # test to see if llm output is valid json 
                try: 
                    question_json = json.loads(question)
                except json.JSONDecodeError:
                    continue

                quiz_question = {
                    "question": question_json,
                    "difficulty": level,
                }

                quiz.append(quiz_question)
    return quiz


def get_details(reading_path, detail_count):
    with open(reading_path, 'r') as f:
        reading = f.readlines()
        reading = ''.join(reading)
    details_json = q_gen.detail_generator(reading, detail_count)

    # test to see if llm output is valid json
    try:
        json.loads(details_json)
    except json.JSONDecodeError:
        raise ValueError("Details are not in valid JSON format")
    # convert json to list
    details = list(json.loads(details_json).values())
    return details
    


def save_quiz(quiz, save_path):
    with open(save_path, 'w') as f:
        json.dump(quiz, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a quiz')
    #parser.add_argument('--details_path', type=str, help='the path to the question details file', required=True)
    # required arguments
    parser.add_argument('--topic', type=str, help='topic of the questions', required=True)
    parser.add_argument('--reading_path', type=str, help='the path to the reading file', required=True)
    # optional arguments
    parser.add_argument('--difficulty', nargs='+', help='a list of strings for the difficulty levels', default=['beginner', 'intermediate', 'expert'])
    parser.add_argument('--detail_count', type=int, help='the number of details to generate', default=20)
    parser.add_argument('--q_per_detail', type=int, help='an integer for the number of questions to generate per detail', default=1)
    parser.add_argument('--save_path', type=str, help='the save path or directory to save the quiz questions to.  If a directory, the quiz questions will be saved to the directory with the name of the topic', default=None)
    # optional arguments for uploading to firebase if save path is not specified
    parser.add_argument('--section', type=str, help='the section of the quiz questions', default=None)
    parser.add_argument('--chapter', type=str, help='the chapter of the quiz questions', default=None)
    args = parser.parse_args()

    q_gen = QuestionGenerator()
    details = get_details(args.reading_path, args.detail_count)
    print(details)
    quiz = quiz_creator(q_gen, details, args.difficulty, args.topic, args.q_per_detail)
    print(quiz)

    # save quiz to file if arg specifies save path
    # else upload quiz to firebase
    if args.save_path is not None:
        if os.path.isdir(args.save_path):
            save_path = os.path.join(args.save_path, f"{args.topic}.json")
        else:
            save_path = args.save_path

        save_quiz(quiz, save_path)
    elif args.section and args.chapter:
        save_questions(quiz, args.section, args.chapter)
    else:
        raise ValueError("No save path or section and chapter specified")
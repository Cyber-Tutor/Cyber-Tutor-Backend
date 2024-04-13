from question_generator import QuestionGenerator
from question_saver import save_questions

from multiprocessing import Pool
import argparse
import json
import os


"""
Generates a quiz based on the reading content and difficulty level
For each detail, it generates a question based on the topic, reading content, and difficulty level
Returns a list of questions in a JSON object
"""
def quiz_creator(q_gen, details, difficulty, topic, q_per_detail=1):
    # get list of question details from file
    quiz = []

    # create questions for each detail based on topic, difficulty
    for detail in details:
        for _ in range(q_per_detail):
            generated = False
            while not generated:
                # pass if question generation fails
                try:
                    question = q_gen.create_question(topic, detail, difficulty)
                except Exception as e:
                    print("Question generation failed: ", e)
                    continue

                # test to see if llm output is valid json 
                try: 
                    question_json = json.loads(question)
                except json.JSONDecodeError:
                    print("Question is not in valid JSON format")
                    continue

                try:
                    keys = question_json['choices'].keys()
                    choices = ["a", "b", "c", "d"]
                    for choice in choices:
                        if choice not in keys:
                            raise KeyError("Choices are not valid")
                except KeyError:
                    print("Choices are not valid", question_json)
                    continue
                
                question = {
                    "question": question_json['question'],
                    "answer": question_json['answer'],
                    "choices": question_json['choices'],
                    "explanation": question_json['explanation'],
                    "difficulty": difficulty
                }
                quiz.append(question)
                generated = True
    return quiz


"""
Generates a list of details based on the reading content
Returns a list of details as a JSON object
"""
def get_details(q_gen, reading, detail_count):
    details_json = q_gen.detail_generator(reading, detail_count)

    # test to see if llm output is valid json
    try:
        json.loads(details_json)
    except json.JSONDecodeError:
        raise ValueError("Details are not in valid JSON format")
    # convert json to list
    details = list(json.loads(details_json).values())
    return details
    

"""
Creates a quiz based on the reading content and difficulty level
Generates a list of details to base questions off of from the reading content
Then it generates a quiz based on the details and reading content
Quiz is saved to a file or uploaded to firebase
"""
def generate_quiz(reading, difficulty, args):
    q_gen = QuestionGenerator()
    name = os.path.basename(args.reading_path)

    print(f"Generating details for {name} at {difficulty} difficulty")
    details = get_details(q_gen, reading, args.detail_count)
    print(f"Details generated for {name} at {difficulty} difficulty")

    print(f"Creating quiz for {name} at {difficulty} difficulty")
    quiz = quiz_creator(q_gen, details, difficulty, args.topic, args.q_per_detail)
    print(f"Quiz created for {name} at {difficulty} difficulty")

    if args.save_path:
        save_path = os.path.join(args.save_path, f"{args.topic}_{difficulty}.json")
        save_quiz(quiz, save_path)
        print(f"Saved quiz locally for {name} at {difficulty} difficulty at {save_path}")
    elif args.section and args.chapter:
        save_questions(quiz, args.section, args.chapter)
        print(f"Saved quiz to firebase for {name} at {difficulty} difficulty")


"""
Saves quiz to json file
"""
def save_quiz(quiz, save_path):
    with open(save_path, 'w') as f:
        json.dump(quiz, f)


"""
Opens reading file and returns content as a string
"""
def open_reading(reading_path):
    with open(reading_path, 'r') as f:
        reading = f.readlines()
        reading = ''.join(reading)
    return reading


"""
Main function for generating quizzes
If reading path is a directory, generates quizzes for all reading difficulties in the directory
If reading path is a file, generates a quiz for the reading file
"""
def main(args):
    if not args.save_path and not args.section and not args.chapter:
        raise ValueError("No save path or section and chapter specified")
    q_gen = QuestionGenerator()
    if os.path.isdir(args.reading_path):
        file_names = []
        gen_args = []
        for file in os.listdir(args.reading_path):
            if file.endswith(".txt"):
                difficulty = "beginner" if "beginner" in file else "intermediate" if "intermediate" in file else "expert" if "expert" in file else None
                if difficulty and difficulty in args.difficulty:
                    # get file for each reading file
                    reading_file_path = os.path.join(args.reading_path, file)
                    reading = open_reading(reading_file_path)
                    file_names.append(file)
                    # create arguments for generating quizzes with multiprocessing
                    gen_args.append((reading, difficulty, args))

        # generate quizzes for all reading files
        with Pool() as p:
            quizzes = p.starmap(generate_quiz, gen_args)
        print("Quizzes created for", *file_names)

    else:
        reading = open_reading(args.reading_path)
        details = get_details(q_gen, reading, args.detail_count)
        file = os.path.basename(args.reading_path)
        difficulty = "beginner" if "beginner" in file else "intermediate" if "intermediate" in file else "expert" if "expert" in file else None
        if difficulty:
            quiz = quiz_creator(q_gen, reading, details, difficulty, args.topic, args.q_per_detail)
            print("Quiz created for", os.path.basename(args.reading_path))
            if args.save_path:
                save_path = os.path.join(args.save_path, f"{args.topic}_{difficulty}.json")
                save_quiz(quiz, save_path)
                print("Quiz saved at", save_path)
            elif args.section and args.chapter:
                save_questions(quiz, args.section, args.chapter)
                print("Quiz saved to firebase")
        else:
            raise ValueError("Difficulty not found in file name")
                

if __name__ == '__main__':
    """
    Creates quiz questions based on provided reading content.  Difficulty is derived from the difficulty specified in the reading file name.
    """
    parser = argparse.ArgumentParser(description='Create a quiz')
    # required arguments
    parser.add_argument('--topic', type=str, help='topic of the questions', required=True)
    parser.add_argument('--reading_path', type=str, help='the path to the reading content directory or file', required=True)
    # optional arguments
    parser.add_argument('--difficulty', nargs='+', help='a list of strings for the difficulty levels', default=['beginner', 'intermediate', 'expert'])
    parser.add_argument('--detail_count', type=int, help='the number of details to generate', default=20)
    parser.add_argument('--q_per_detail', type=int, help='an integer for the number of questions to generate per detail', default=1)
    parser.add_argument('--save_path', type=str, help='the save path or directory to save the quiz questions to.  If a directory, the quiz questions will be saved to the directory with the name of the topic', default=None)
    # optional arguments for uploading to firebase if save path is not specified
    parser.add_argument('--section', type=str, help='the section of the quiz questions', default=None)
    parser.add_argument('--chapter', type=str, help='the chapter of the quiz questions', default=None)
    args = parser.parse_args()
    main(args)
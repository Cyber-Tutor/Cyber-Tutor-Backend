from flask import Flask, jsonify, request, abort
from llm import invoke_llm
from firebase import Firebase
import random

app = Flask(__name__)
db = Firebase()


# /get_quiz route
# get quiz for given section/chapter and user
# parameters: section, chapter, user id
@app.route('/get_quiz', methods=['GET'])
def get_quiz():
    section = request.args.get('section', None)
    chapter = request.args.get('chapter', None)
    user_id = request.args.get('user_id', None)
    count = request.args.get('count', 10)
    # check for missing parameters - return 400 if any are missing
    if None in [section, chapter, user_id]:
        abort(400)

    # get user group
    group = db.user_group(user_id)
    # get questions based on section, chapter, and group
    quiz = db.get_quiz_questions(section, chapter, group)
    # if experimental: filter questions based on user's proficiency (ratio)
    # if control: return all questions
    # limit questions to count
    # return quiz
    if group == 'experimental':
        pass
    else:
        pass
    return jsonify({'questions': quiz})


# /get_test route
# get test for given section/chapter and user
# parameters: section, chapter, user id
# TODO: implement experimental group filtering
@app.route('/get_test', methods=['GET'])
def get_test():
    section = request.args.get('section', None)
    chapter = request.args.get('chapter', None)
    user_id = request.args.get('user_id', None)
    count = request.args.get('count', 25)
    # check for missing parameters - return 400 if any are missing
    if None in [section, chapter, user_id]:
        abort(400)

    # get user group
    group = db.user_group(user_id)
    # get questions based on section, chapter, and group
    questions = db.get_test_questions(section, chapter, group)
    # if experimental: filter questions based on user's proficiency (ratio)
    # if control: return all questions
    # limit questions to count
    # return quiz
    if group == 'experimental':
        pass
    else:
        # get random questions of given count
        test = random.sample(questions, count)
    return jsonify({'questions': test})


# /get_reading route
# get reading content for given section/chapter and user
# parameters: section, chapter, user id
@app.route('/get_reading', methods=['GET'])
def reading():
    section = request.args.get('section', None)
    chapter = request.args.get('chapter', None)
    user_id = request.args.get('user_id', None)
    # check for missing parameters - return 400 if any are missing
    if None in [section, chapter, user_id]:
        abort(400)

    # get user group
    group = db.user_group(user_id)
    # get reading content based on section, chapter, and group
    reading = db.get_reading(section, chapter, group)
    return jsonify({'reading': reading})


# /submit_quiz route
# submit quiz for given section/chapter and user
# parameters: section, chapter, user id, quiz, answers
@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    section = request.args.get('section', None)
    chapter = request.args.get('chapter', None)
    user_id = request.args.get('user_id', None)
    quiz = request.args.get('quiz', None)
    answers = request.args.get('answers', None)
    # check for missing parameters - return 400 if any are missing
    if None in [section, chapter, user_id, quiz, answers]:
        abort(400)

    score = 0
    correct = 0
    total = len(quiz)
    # check answers
    for i, question in enumerate(quiz):
        if db.check_quiz_answer(question, answers[i]):
            correct += 1
    # calculate score
    score = round(correct / total, 2)
    # save score to user's profile
    db.save_quiz_score(user_id, section, chapter, score)
    # return score
    return jsonify({'score': score})


# /submit_test route
# submit test for given section and user
# parameters: section, user id, test, answers
@app.route('/submit_test', methods=['POST'])
def submit_test():
    section = request.args.get('section', None)
    user_id = request.args.get('user_id', None)
    test = request.args.get('test', None)
    answers = request.args.get('answers', None)
    # check for missing parameters - return 400 if any are missing
    if None in [section, user_id, test, answers]:
        abort(400)

    score = 0
    correct = 0
    total = len(test)
    # check answers
    for i, question in enumerate(test):
        if db.check_test_answer(question, answers[i]):
            correct += 1
    # calculate score
    score = round(correct / total, 2)
    # save score to user's profile
    db.save_test_score(user_id, section, score)
    # return score
    return jsonify({'score': score})
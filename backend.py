from flask import Flask, jsonify, request, abort
from llm import invoke_llm
from firebase import Firebase

app = Flask(__name__)
db = Firebase()

@app.route('/invoke', methods=['POST'])
def invoke():
    prompt = request.json['prompt']
    return jsonify({'response': invoke_llm(prompt)})

@app.route('/generate_reading', methods=['POST'])
def generate_reading():
    topic = request.json['topic']
    word_count = request.json['word_count']
    return jsonify({'response': generate_reading(topic, word_count)})


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
@app.route('/get_test', methods=['GET'])
def get_test():
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
    test = db.get_test_questions(section, chapter, group)
    # if experimental: filter questions based on user's proficiency (ratio)
    # if control: return all questions
    # limit questions to count
    # return quiz
    if group == 'experimental':
        pass
    else:
        pass
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
    ## get user group
    ##group = db.user_group(user_id)
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
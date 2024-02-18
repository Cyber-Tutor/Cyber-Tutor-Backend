from flask import Flask, jsonify, request
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
def quiz():
    section = request.args.get('section')
    chapter = request.args.get('chapter')
    user_id = request.args.get('user_id')
    count = request.args.get('count')
    # get user group
    group = db.user_group(user_id)
    # get questions based on section, chapter, and group
    questions = db.get_quiz_questions(section, chapter, group)
    # if experimental: filter questions based on user's proficiency (ratio)
    # if control: return all questions
    # limit questions to count
    # return quiz
    return jsonify({'questions': questions})


# /get_test route
# get test for given section/chapter and user
# parameters: section, chapter, user id
@app.route('/get_test', methods=['GET'])
def test():
    section = request.args.get('section')
    chapter = request.args.get('chapter')
    user_id = request.args.get('user_id')
    count = request.args.get('count')
    # get user group
    group = db.user_group(user_id)
    # get questions based on section, chapter, and group
    questions = db.get_test_questions(section, chapter, group)
    # if experimental: filter questions based on user's proficiency (ratio)
    # if control: return all questions
    # limit questions to count
    # return quiz
    return jsonify({'questions': questions})


# /get_reading route
# get reading content for given section/chapter and user
# parameters: section, chapter, user id
@app.route('/get_reading', methods=['GET'])
def reading():
    section = request.args.get('section')
    chapter = request.args.get('chapter')
    user_id = request.args.get('user_id')
    # get user group
    group = db.user_group(user_id)
    # get reading content based on section, chapter, and group
    reading = db.get_reading(section, chapter, group)
    return jsonify({'reading': reading})


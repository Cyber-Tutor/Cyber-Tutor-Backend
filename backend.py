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

# get experimental quiz for given section/chapter and user
# parameters: section, chapter, user id
@app.route('/get_quiz', methods=['GET'])
def quiz():
    section = request.args.get('section')
    chapter = request.args.get('chapter')
    user_id = request.args.get('user_id')
    # get user group
    # get quiz from database depending on group
    # get user's proficiency in section
    # get ratio of questions based on proficiency
    # get questions from database
    # return quiz
    return jsonify({'questions': None})


# route getting reading for given section/chapter
# route getting quiz for given section/chapter
# route for submitting quiz answers
# route for getting quiz results
# content generator

# are we storing grades of quizzes or the questions they got wrong
# database needs user table - what is stored here
# database needs quiz pool
# am i sending the quiz and quiz results to frontend (and grading happens there) or am i grading on the backend
# are we not repeating questions in the quiz from previous quizzes

# no videos section in database

# add proficiency to question and other metadata

# ratio should be stored in db
# db structure is a nightmare to work with
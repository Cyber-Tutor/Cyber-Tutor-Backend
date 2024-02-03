from flask import Flask, jsonify, request
from llm import invoke_llm

app = Flask(__name__)


@app.route('/invoke', methods=['POST'])
def invoke():
    prompt = request.json['prompt']
    return jsonify({'response': invoke_llm(prompt)})

@app.route('/generate_reading', methods=['POST'])
def generate_reading():
    topic = request.json['topic']
    word_count = request.json['word_count']
    return jsonify({'response': generate_reading(topic, word_count)})

# TODO: Implement this
@app.route('/get_quiz', methods=['GET'])
def quiz():
    return jsonify({'questions': None})
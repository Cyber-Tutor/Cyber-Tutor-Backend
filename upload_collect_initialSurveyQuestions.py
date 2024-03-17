import re
import firebase_admin
from firebase_admin import credentials, firestore
import json

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def to_snake_case(text):
    text = re.sub(r"[\s\-]+", " ", text)
    components = text.split(" ")
    return "_".join(x.lower() for x in components)


def to_camel_case(text):
    text = re.sub(r"[\-\.\s]", "_", text)
    components = text.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


with open("data/initialSurveyQuestions.json") as f:
    data = json.load(f)

for category, questions in data.items():
    for question_id, question_details in questions.items():
        snake_case_question_id = to_snake_case(question_id)
        doc_ref = db.collection("initialSurveyQuestions").document(snake_case_question_id)

        doc_data = {}

        # This only adds it if it exists, if not, it skips it
        if question_details.get("question"):
            doc_data["question"] = question_details["question"]
        if question_details.get("questionCategory"):
            doc_data["questionCategory"] = question_details["questionCategory"]
        if question_details.get("questionType"):
            doc_data["questionType"] = question_details["questionType"]
        if question_details.get("choices"):
            doc_data["choices"] = question_details["choices"]
        if question_details.get("answer"):
            doc_data["answer"] = question_details["answer"]
        if question_details.get("difficulty"):
            doc_data["difficulty"] = question_details["difficulty"]
        if question_details.get("explanation"):
            doc_data["explanation"] = question_details["explanation"]

        doc_ref.set(doc_data)

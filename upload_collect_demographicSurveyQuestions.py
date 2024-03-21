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

with open("data/demographicsurvey.json") as f:
    data = json.load(f)

for category, questions in data.items():
    for question_id, question_details in questions.items():
        snake_case_question_id = to_snake_case(question_id)
        doc_ref = db.collection("demographicSurveyQuestions").document(snake_case_question_id)

        doc_data = {
            "isRequired": True  # Set the isRequired property for each question
        }

        # This only adds it if it exists, if not, it skips it
        if question_details.get("question"):
            doc_data["question"] = question_details["question"]
        if question_details.get("choices"):
            doc_data["choices"] = question_details["choices"]
        if question_details.get("questionType"):  # Ensuring the questionType is included if provided
            doc_data["questionType"] = question_details["questionType"]

        doc_ref.set(doc_data)

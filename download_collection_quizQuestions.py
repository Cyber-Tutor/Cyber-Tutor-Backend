import firebase_admin
from firebase_admin import credentials, firestore
import json


def download_quiz_questions(output_file_path, db):
    all_questions = db.collection("quizQuestions").stream()

    questions_list = []
    for question in all_questions:
        question_dict = question.to_dict()
        question_dict["questionId"] = question.id
        questions_list.append(question_dict)

    with open(output_file_path, "w") as f:
        json.dump({"quizQuestions": questions_list}, f, indent=4)


if __name__ == "__main__":
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    output_file_path = "quizQuestions.json"

    download_quiz_questions(output_file_path, db)

    print(f"Quiz questions downloaded successfully to {output_file_path}")

import json
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def upload_quiz_questions(input_file_path, db):
    with open(input_file_path) as f:
        data = json.load(f)

    for question in data["quizQuestions"]:
        question_data = {
            key: val
            for key, val in question.items()
            if key
            in [
                "question",
                "choices",
                "answer",
                "topicId",
                "chapterId",
                "difficulty",
                "explanation",
                "topics",
                "fromChapter",
                "isHumanWritten",
            ]
        }
        db.collection("quizQuestions").add(question_data)


if __name__ == "__main__":
    input_file_path = "quizQuestions.json"

    upload_quiz_questions(input_file_path, db)

    print(f"Quiz questions uploaded successfully from {input_file_path}")

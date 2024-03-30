import re
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def to_snake_case(text):
    text = re.sub(r"[\s\-]+", "_", text)
    return "_".join(x.lower() for x in text.split("_"))


def upload_data(file_path):
    with open(file_path) as f:
        data = json.load(f)

    for topic_details in data["topics"]:
        topic_id = to_snake_case(topic_details["topicTitle"])
        topic_ref = db.collection("topics").document(topic_id)
        topic_ref.set(
            {
                "topicDescription": topic_details["topicDescription"],
                "topicTitle": topic_details["topicTitle"],
                "order": topic_details["order"],
            }
        )

        chapters_ref = topic_ref.collection("chapters")
        for chapter_details in topic_details["chapters"]:
            chapter_id = to_snake_case(chapter_details["chapterTitle"])
            chapter_ref = chapters_ref.document(chapter_id)

            chapter_data = {
                key: val
                for key, val in chapter_details.items()
                if key
                in [
                    "chapterType",
                    "chapterDescription",
                    "chapterTitle",
                    "controlGroupContent",
                    "experimentalGroupContent",
                    "controlGroupImageURLs",
                    "experimentalGroupImageURLs",
                    "order",
                    "proficiency",
                ]
            }

            chapter_ref.set(chapter_data)


if __name__ == "__main__":
    upload_data("data/topics6.json")

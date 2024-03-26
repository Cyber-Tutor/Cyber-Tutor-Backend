import re
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firebase
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


# def clean_quiz_title(title):
#     if "Quiz" in title:
#         return title.replace(":", "")
#     return title


with open("data/topics5.json") as f:
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
        # chapter_details["chapterTitle"] = clean_quiz_title(
        #     chapter_details["chapterTitle"]
        # )
        chapter_id = to_snake_case(chapter_details["chapterTitle"])
        chapter_ref = chapters_ref.document(chapter_id)
        chapter_ref.set(
            {
                "chapterType": chapter_details["chapterType"],
                "chapterDescription": chapter_details["chapterDescription"],
                "chapterTitle": chapter_details["chapterTitle"],
                "controlGroupContent": chapter_details["controlGroupContent"],
                "experimentalGroupContent": chapter_details["experimentalGroupContent"],
                "controlGroupImageURL": chapter_details["controlGroupImageURL"],
                "experimentalGroupImageURL": chapter_details[
                    "experimentalGroupImageURL"
                ],
                "order": chapter_details["order"],
                "proficiency": chapter_details["proficiency"],
            }
        )

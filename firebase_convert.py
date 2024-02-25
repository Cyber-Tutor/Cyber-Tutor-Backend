import firebase_admin
from firebase_admin import credentials, firestore
import json

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def extract_chapter_info(chapters):
    extracted_info = {}
    for chapter_id, chapter_details in chapters.items():
        extracted_info[chapter_id] = {
            "chapterType": chapter_details["chapterType"],
            "chapterDescription": chapter_details["chapterDescription"],
            "chapterTitle": chapter_details["chapterTitle"],
        }
        control_group_content = {}
        experimental_group_content = {}
        for subchapter_id, subchapter_details in chapter_details.get(
            "controlGroup", {}
        ).items():
            control_group_content[subchapter_id] = subchapter_details.get(
                "chapterContent", ""
            )
        for subchapter_id, subchapter_details in chapter_details.get(
            "experimentalGroup", {}
        ).items():
            experimental_group_content[subchapter_id] = subchapter_details.get(
                "chapterContent", ""
            )
        extracted_info[chapter_id]["controlGroupContent"] = control_group_content
        extracted_info[chapter_id][
            "experimentalGroupContent"
        ] = experimental_group_content
    return extracted_info


with open("data.json") as f:
    data = json.load(f)


for topic_id, topic_details in enumerate(data["topics"]):
    topic_ref = db.collection("topics").document(str(topic_id))
    topic_ref.set(
        {
            "topicDescription": topic_details["description"],
            "topicTitle": topic_details["title"],
        }
    )

    chapters_ref = topic_ref.collection("chapters")
    for chapter_id, chapter_details in enumerate(topic_details["chapters"]):
        chapter_ref = chapters_ref.document(str(chapter_id))
        chapter_ref.set(
            {
                "chapterType": chapter_details["type"],
                "chapterDescription": chapter_details["description"],
                "chapterTitle": chapter_details["title"],
                "controlGroupContent": chapter_details["controlGroupContent"],
                "experimentalGroupContent": chapter_details["experimentalGroupContent"],
                "controlGroupImageURLs": chapter_details.get(
                    "controlGroupImageURLs", []
                ),
                "experimentalGroupImageURLs": chapter_details.get(
                    "experimentalGroupImageURLs", []
                ),
            }
        )

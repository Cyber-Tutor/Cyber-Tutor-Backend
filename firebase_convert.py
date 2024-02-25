import firebase_admin
from firebase_admin import credentials, firestore
import json


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


db = firestore.client()


def extract_chapter_info(chapters):
    extracted_info = {}
    for chapter_key, chapter_details in chapters.items():
        extracted_info[chapter_key] = {
            "chapterType": chapter_details["chapterType"],
            "chapterDescription": chapter_details["chapterDescription"],
            "chapterTitle": chapter_details["chapterTitle"],
        }
    return extracted_info


f = open("data.json")
data = json.load(f)

update_data = {}
for key, value in data.items():
    if key != "0":
        update_data[key] = {
            "topicDescription": value["topicDescription"],
            "topicId": value["topicId"],
            "topicTitle": value["topicTitle"],
            "chapters": extract_chapter_info(value["chapters"]),
            "controlGroup": {},
            "experimentalGroup": {},
        }

# print(json.dumps(update_data, indent=2))


doc_ref = db.collection("cyber-tutor").document("topics")


for key, value in update_data.items():
    doc_ref.set({key: value}, merge=True)

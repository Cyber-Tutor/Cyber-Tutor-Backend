import firebase_admin
from firebase_admin import credentials, firestore
import json


def download_data(output_file_path, db):
    all_topics = db.collection("topics").stream()

    topics_list = []
    for topic in all_topics:
        topic_dict = topic.to_dict()
        topic_dict["topicId"] = topic.id

        chapters_ref = db.collection("topics").document(topic.id).collection("chapters")
        chapters = chapters_ref.stream()

        chapters_list = []
        for chapter in chapters:
            chapter_dict = chapter.to_dict()
            chapter_dict["chapterId"] = chapter.id
            chapters_list.append(chapter_dict)

        sorted_chapters = sorted(chapters_list, key=lambda x: x.get("order", 0))
        topic_dict["chapters"] = sorted_chapters

        topics_list.append(topic_dict)

    sorted_topics = sorted(topics_list, key=lambda x: x.get("order", 0))

    with open(output_file_path, "w") as f:
        json.dump({"topics": sorted_topics}, f, indent=4)


if __name__ == "__main__":
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    output_file_path = "topics.json"

    download_data(output_file_path, db)

    print(f"Data downloaded successfully to {output_file_path}")

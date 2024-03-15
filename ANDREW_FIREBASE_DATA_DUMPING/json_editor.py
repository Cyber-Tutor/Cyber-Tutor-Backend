import json

with open("data/topics2.json", "r") as file:
    data = json.load(file)

for topic in data["topics"]:
    for chapter in topic["chapters"]:
        chapter["proficiency"] = 0

with open("data/topics3.json", "w") as file:
    json.dump(data, file, indent=4)

import json

with open("quizQuestions.json", "r") as file:
    data = json.load(file)

for question in data["quizQuestions"]:
    question["isHumanWritten"] = 0

with open("quizQuestions_updated.json", "w") as file:
    json.dump(data, file, indent=4)

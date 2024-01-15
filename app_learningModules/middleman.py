from configparser import ConfigParser
import google.generativeai as genai
from dotenv import load_dotenv
import os 

load_dotenv()
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
model_gemini_pro = genai.GenerativeModel('gemini-pro')

prompt = """ Return in this JSON format with a randome number of questions
{
    "title": "CyberTutor Proficiency Quiz",
    "logoFit": "none",
    "logoPosition": "right",
    "pages": [
     {
      "name": "page1",
      "elements": [
       {
        "type": "radiogroup",
        "name": "Fundamental Concepts and Princicples",
        "title": "Is knowledge of cybersecurity important for everyone?",
        "isRequired": true,
        "choices": [
         "Yes",
         "No",
         "Maybe",
         "Who cares"
        ],
        "choicesOrder": "random",
        "showClearButton": true
       }
      ],
      "readOnly": false,
      "title": "Question 1",
      "description": "Fundamental Concepts and Principles"
     }
    ],
    "triggers": [
     {
      "type": "runexpression"
     }
    ],
    "widthMode": "responsive",
    "fitToContainer": true
   }"""

response = model_gemini_pro.generate_content(prompt)
print(response.text)
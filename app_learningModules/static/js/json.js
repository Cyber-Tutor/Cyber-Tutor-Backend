const json = {
    "title": "Your Survey Title",
    "description": "Your survey description goes here.",
    "pages": [
      {
        "name": "page1",
        "elements": [
          {
            "type": "text",
            "name": "question1",
            "title": "Your question text goes here"
          },
          {
            "type": "checkbox",
            "name": "question2",
            "title": "Your question text goes here",
            "choices": [
              "Answer option 1",
              "Answer option 2",
              "Answer option 3"
            ]
          }
          // Add more questions here
        ]
      }
      // Add more pages here
    ],
    "completedHtml": "<h3>Thank you for completing the survey!</h3><h5>Your feedback is appreciated.</h5>"
  }
  

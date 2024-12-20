# Gemini: A Personalized AI-Powered Cybersecurity Education Tool

## Project Overview
Gemini is a proof-of-concept web application designed to deliver personalized cybersecurity training content to users based on their knowledge, awareness, and behavioral habits. The tool dynamically tailors content to meet individual proficiency levels, ensuring a highly customized learning experience. It utilizes Google Gemini AI to recommend cybersecurity materials such as videos, articles, and tips, allowing users to stay safe online and enhance their knowledge.

## Key Features
1. **User Proficiency Assessment**: Users complete an initial survey that evaluates their cybersecurity awareness and habits.
2. **AI-Driven Personalization**: The survey responses are processed by Google Gemini AI, which determines the user's proficiency level (Beginner, Intermediate, Expert).
3. **Dynamic Content Delivery**: Based on the user's proficiency, the app recommends curated content tailored to their level.

## Application Workflow
### User Proficiency Determination Flow
1. **User Responses Collected**:
   - Users take an assessment survey to evaluate their current cybersecurity knowledge, awareness, and behavioral habits.
   - The survey collects insights into their behaviors and practices.

2. **Response Processing**:
   - Survey responses are passed to Google Gemini AI.
   - The AI determines the user's proficiency level and categorizes the user as Beginner, Intermediate, or Expert.

3. **Personalized Output**:
   - Topics relevant to the user’s proficiency are extracted.
   - These topics are saved in Firebase and linked to the user’s profile for future recommendations.

### Content Generation Flow
1. **Information Storage**:
   - Content from reputable sources (e.g., consumer.ftc.gov, cyber.org, security.org) is stored in a vector database.
   - This database establishes relationships between content topics, enabling efficient querying.

2. **Reading Generation**:
   - Gemini creates content tailored to varying difficulty levels to ensure accuracy and relevance.

3. **Question Generation**:
   - Questions and answers are generated based on the reading content.
   - Multiple-choice quizzes with explanations for correct answers are provided.

4. **Output Delivery**:
   - The app displays tailored educational content, including articles, videos, and tips, designed for the user’s specific proficiency level.

## Technology Stack
### Frontend
- **Next.js**:
  - Used for efficient file-based routing and seamless integration with SurveyJS for form creation.

### Backend
- **Python & Google Gemini AI**:
  - Powers personalized content generation and quiz creation.

### Database
- **Firebase Firestore Database**:
  - Non-relational storage for user data and content, offering built-in authentication.

### Image Generation
- **ChatGPT**:
  - Generates synthesized descriptions and titles.

### Video Generation
- **Invideo**:
  - Transforms text-based content into videos using AI.

## Future Work
- **Comprehensive User Testing**: Conduct studies to validate the effectiveness of AI-generated educational content compared to traditional methods.
- **Enhanced Analytics**: Leverage user feedback to refine recommendations and improve learning outcomes.
- **Expanded Use Cases**: Explore Gemini’s potential in broader educational applications.

## References
- [ai.google.dev](https://ai.google.dev)
- [nextjs.org](https://nextjs.org)
- [consumer.ftc.gov](https://consumer.ftc.gov)
- [cyber.org](https://cyber.org)
- [security.org](https://security.org)
- And 54 more sources.



Since our project uses Django 5.0, Python 3.10 or later is required for installation.

In Visual Studio Code:
1) Clone the GitHub repository
2) Create, and activate, a virutal environment
    ## Linux
    ```bash
        sudo apt-get install python3-venv
        python3 -m venv .venv
        source .venv/bin/activate
    ```
    ## macOS
    ```bash
        python3 -m venv .venv
        source .venv/bin/activate
    ```
    ## Windows
    ```bash
        py -3 -m venv .venv
        .venv\scripts\activate
    ```
3) Select interpreter:
- CTRL + SHIFT + P
- Select: Python: Select Interpreter
- Select: Interpreter path that starts with ```./.venv``` or ```.\.venv```
4) Install project dependencies:
  ```bash
   pip install -r requirements.txt
  ```
5) Set up .env file
- Create .env file in root, where manage.py is located
- ```bash
  SECRET_KEY = 'STEP 6'
  GEMINI_API_KEY = ''
  POSTGRES_PASSWORD = ''
  AWS_ENDPOINT_URL = ''
  ```
6) Generate your SECRET_KEY
- CTRL + SHIFT + `
- ```bash
  python
  ``` 
- ```bash
  from django.core.management.utils import get_random_secret_key
  print(get_random_secret_key())
  ```
- Copy, and paste that into your .env, where you see 'STEP 6'
7) Apply migrations to the database
  ```bash
  python manage.py migrate
  ```
8) Run the development server:
  ```bash
  python manage.py runserver
  ```

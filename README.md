# NewResearchProject

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
  CHATGPT_API_KEY = '<YOUR CHAT GPT API KEY>'
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
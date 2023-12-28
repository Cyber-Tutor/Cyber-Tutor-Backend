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
- IN-PROGRESS
6) Run the development server:
  ```bash
  python manage.py runserver
  ```
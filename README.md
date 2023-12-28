# NewResearchProject

```bash
In Visual Studio Code:
1) Clone the GitHub repository
2) Create, and activate, a virutal environment
    a)  # Linux
        sudo apt-get install python3-venv
        python3 -m venv .venv
        source .venv/bin/activate

    b) # macOS
        python3 -m venv .venv
        source .venv/bin/activate

    c) # Windows
        py -3 -m venv .venv
        .venv\scripts\activate
3) Select interpreter:
    a) 'CTRL + SHIFT + P'
    b) Select: 'Python: Select Interpreter'
    c) Select: Interpreter path that starts with './.venv' or '.\.venv'
4) Install project dependencies:
    a) pip install -r requirements.txt 
5) Set up .env file
    a) IN-PROGRESS
6) Run the development server:
    a) 'python manage.py runserver'
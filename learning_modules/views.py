from django.shortcuts import render
import os 
from openai import OpenAI
CHATGPT_API_KEY = os.environ['CHATGPT_API_KEY']

client  = OpenAI(api_key=CHATGPT_API_KEY)

def content(request):
    result = ''
    if request.method == "POST":
        question = request.POST.get('question')
        if question:
            try:
                # Use the client to create a chat completion
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # Make sure to use the correct chat model
                    messages=[{"role": "user", "content": question}]
                )
                # Access the response attributes
                result = response.choices[0].message.content
            except Exception as e:  # Catch any exceptions from the API call
                result = f"An error occurred: {str(e)}"
    return render(request, 'content.html', {'result': result})
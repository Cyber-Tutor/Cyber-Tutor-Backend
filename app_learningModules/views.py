from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Course, Module
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

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

# Grabs modules associated with specified course. Then it converts it to a list 
# of dictionaries, then passed to client as a JSON response that we can use in 
# our JavaScript.
def get_modules_for_course(request, course_id):
    modules = Module.objects.filter(course_id=course_id).order_by('order')
    modules_data = list(modules.values('id', 'title', 'description'))
    return JsonResponse(modules_data, safe=False)

def module_detail(request, course_id, module_number):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, course=course)
    return render(request, 'module_detail.html', {'course': course, 'module': module})


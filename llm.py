from langchain_google_genai import GoogleGenerativeAI
import os

def invoke_llm(prompt):
    llm = GoogleGenerativeAI(model=os.environ['LLM_MODEL'])
    return llm.invoke(prompt)

def generate_reading(topic, word_count=500):
    prompt = f"Write a reading about {topic} in {word_count} words."
    return invoke_llm(prompt)
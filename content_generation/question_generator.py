from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate

import dotenv
import os

dotenv.load_dotenv()


class QuestionGenerator:
    def __init__(self):
        self.chain = self.initialize()

    def create_question(self, topic, details, difficulty):
        prompt_template = PromptTemplate.from_template("""
        Write a multiple choice question (a, b, c, d) about {topic}, specifically {details} that is targeted towards a difficulty of {difficulty}.
        Format the response as a JSON object with the following keys:
        - "question": The question you want to ask
        - "answer": The correct answer to the question, either "a", "b", "c", or "d"
        - "choices": keys of a, b, c, d with the answer choices.
        - "explanation": An explanation of the correct answer.
        - "topics": A list of topics that the question covers.
        Do not repeat answer choices.  Do not make answer choices too similar to each other.
        The "answer" key MUST be one of the choices in the "choices" list.
        """)

        result = self.chain(prompt_template.format(topic=topic, details=details, difficulty=difficulty))
        return result['result']


    def initialize(self):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", convert_system_message_to_human=True)
        db = Chroma(persist_directory=os.environ['CHROMA_PATH'], embedding_function=embeddings)
        
        retriever = db.as_retriever()
        llm = ChatGoogleGenerativeAI(model=os.environ['LLM_MODEL'], convert_system_message_to_human=True)
        
        chain = RetrievalQA.from_chain_type(
            llm,
            retriever=retriever
        )

        return chain

if __name__ == '__main__':
    q_gen = QuestionGenerator()
    print(q_gen.create_question("2fa", "what it is", "easy"))
    print(q_gen.create_question("phishing", "what it is", "easy"))
    print(q_gen.create_question("password management", "best practices", "easy"))
    print(q_gen.create_question("online security", "best practices", "easy"))
    print(q_gen.create_question("2fa", "what it is", "medium"))
    print(q_gen.create_question("phishing", "what it is", "medium"))
    print(q_gen.create_question("password management", "best practices", "medium"))
    print(q_gen.create_question("online security", "best practices", "medium"))
    print(q_gen.create_question("2fa", "what it is", "hard"))
    print(q_gen.create_question("phishing", "what it is", "hard"))
    print(q_gen.create_question("password management", "best practices", "hard"))
    print(q_gen.create_question("online security", "best practices", "hard"))
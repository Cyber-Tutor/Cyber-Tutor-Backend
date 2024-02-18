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

    def create_reading(self, topic, word_count=500):
        prompt_template = PromptTemplate.from_template("""
        Write a detailed article explaining {topic} in {word_count} words.
        """)

        result = self.chain(prompt_template.format(topic=topic, word_count=word_count))
        return result


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
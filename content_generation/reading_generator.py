from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate

import dotenv
import os

dotenv.load_dotenv()


class ReadingGenerator:
    def __init__(self):
        self.chain = self.initialize()

    """
    create reading based on topic, content (list of points to include in the reading), and optional word count
    """
    def create_reading(self, topic, content, word_count=500):
        content = ', '.join(content)

        prompt_template = PromptTemplate.from_template("""
        Write a detailed article explaining {topic} in {word_count} words. 
        Make sure to include content on the following topics: {content}                                        
        """)

        result = self.chain(prompt_template.format(topic=topic, word_count=word_count, content=content))
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
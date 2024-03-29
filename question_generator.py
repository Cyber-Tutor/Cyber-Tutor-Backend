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
        Do not repeat answer choices.  Do not make answer choices too similar to each other.
        The "answer" key MUST be one of the choices in the "choices" list.
        """)

        result = self.chain(prompt_template.format(topic=topic, details=details, difficulty=difficulty))
        
        # return question if no error in generation occurred
        try:
            return result['result']
        except:
            return None


    def detail_generator(self, reading, count):
        prompt_template = PromptTemplate.from_template(f"""
            You are to read the following article.  Generate {count} details that could be used to create quiz questions based on the reading.  
            Do not generate quiz questions, only content that will be used in later prompts to generate the questions.
            Output the details as a JSON object with the keys for each detail being the index of the detail. Do not add ```json``` to the output.
            If there are multiple details in a single line, separate them with a comma.
            Keep the details contained to a single line.
            Do not capitalize the first letter of the details.
            Use any and all relevant information from the article to generate the details.
            An example looks like: what is 2FA, specifically what type of methods are available
            See the article below:

            {reading}
            """
        )
        details = self.chain(prompt_template.format(count=count, reading=reading))
        try:
            return details['result']
        except:
            return None
        

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
    print(q_gen.create_question("online security", "best practices", "hard"))
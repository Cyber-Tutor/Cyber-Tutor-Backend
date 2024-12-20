from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

import dotenv
import os

dotenv.load_dotenv()


"""
QuestionGenerator class that handles generating questions and details
It uses the Chroma database as context for question and detail generation.
Details are topics that questions are based on, generated from reading content
Questions are generated based on the topic, generated details, and difficulty level. 
"""
class QuestionGenerator:
    def __init__(self):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", convert_system_message_to_human=True)
        self.db = Chroma(persist_directory=os.environ['CHROMA_PATH'], embedding_function=embeddings)
        
        self.retriever = self.db.as_retriever()
        self.llm = ChatGoogleGenerativeAI(model=os.environ['LLM_MODEL'], convert_system_message_to_human=True)

    """
    Generates multiple choice questions based on a topic, details, and difficulty level
    It generates as many questions as there are details, with each question targeting a specific detail
    Returns questions in a JSON object with the key "questions" containing a list of questions
    """
    def create_question(self, reading, topic, detail, difficulty):
        prompt_template = PromptTemplate.from_template("""
        You are given the following context: {context}.     
        Base the question on the following reading: """ + reading + """"       
        Write a multiple choice question (a, b, c, d) about """ + topic + """, targeted towards a difficulty of """ + difficulty + """.
        The question should specifically be about """ + detail + """.
        Format the response as a JSON object.  The JSON object with the following keys:
        - "question": The question you want to ask
        - "answer": The correct answer to the question, either "a", "b", "c", or "d"
        - "choices": keys of a, b, c, d with the answer choices.
        - "explanation": An explanation of the correct answer.
        Do not add ```json``` to the output.
        Do not repeat answer choices.  Do not make answer choices too similar to each other.
        The "answer" key MUST be one of the choices in the "choices" list.
        """)

        retriever = self.db.as_retriever()

        chain = (
            {"context": retriever}
            | prompt_template
            | self.llm
            | StrOutputParser()
        )

        result = chain.invoke(detail)
        # return question if no error in generation occurred
        try:
            return result
        except:
            return None


    """
    Generates question details based on provided reading
    Returns details in a JSON object with the index of the detail as the key
    """
    def detail_generator(self, reading, count):
        chain = RetrievalQA.from_chain_type(
            self.llm,
            retriever=self.retriever
        )        

        prompt_template = PromptTemplate.from_template(f"""
            You are to read the following article.  Generate {count} details that could be used to create quiz questions based on the reading.  
            Do not generate quiz questions, only content that will be used in later prompts to generate the questions.
            Output the details as a JSON object with the keys for each detail being the index of the detail. Do not add ```json``` to the output.
            If there are multiple details, separate them with a comma.
            Do not capitalize the first letter of the details.
            Use any and all relevant information from the article to generate the details.
            An example looks like: what is 2FA, specifically what type of methods are available
            See the article below:

            {reading}
            """
        )
        details = chain(prompt_template.format(count=count, reading=reading))
        try:
            return details['result']
        except:
            return None
        

if __name__ == '__main__':
    q_gen = QuestionGenerator()
    print(q_gen.create_questions("online privacy", ["best practices", "how to stay secure"], "expert"))
    
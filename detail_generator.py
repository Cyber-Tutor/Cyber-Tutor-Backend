from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
import os
import argparse
import dotenv

dotenv.load_dotenv()


class DetailGenerator:
    def __init__(self):
        self.chain = self.initialize()

    def load_reading(self, path):
         with open(path, 'r') as f:
            return f.readlines()
         
    def save_details(self, details, path):
        with open(path, 'w') as f:
            f.write(details)
    
    """
    Create details based on reading at reading_path, save to details_path
    """
    def create_details(self, reading_path, count):
        reading = self.load_reading(reading_path)
        reading = ''.join(reading)

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
            """)
        result = self.chain(prompt_template.format(reading=reading))

        try:
            details = result['result']                                      
        except:
            ValueError("Error in generating details")

        return details

    def initialize(self):
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", convert_system_message_to_human=True)
            db = Chroma(persist_directory=os.environ['CHROMA_PATH'], embedding_function=embeddings)
            
            retriever = db.as_retriever()
            llm = ChatGoogleGenerativeAI(model=os.environ['LLM_MODEL'], convert_system_message_to_human=True, temperature=0.3, top_p=0.9)
            
            chain = RetrievalQA.from_chain_type(
                llm,
                retriever=retriever
            )

            return chain
    

if __name__ == '__main__':
    """
    Generate details to generate quiz questions from a reading.
    Provide a reading path and a details directory to save the details to.
    If the reading path is a directory, it generates details for all reading in the directory.
    """
    parser = argparse.ArgumentParser(description='Reading details generator.')
    parser.add_argument('--reading_path', type=str, help='reading path for a file or directory containing readings', required=True)
    parser.add_argument('--details_dir', type=str, help='directory to save details to', required=True)
    parser.add_argument('--detail_count', type=int, help='number of details to generate', default=25)

    args = parser.parse_args()
    dg = DetailGenerator()

    if os.path.isdir(args.reading_path):
        for file in os.listdir(args.reading_path):
            if file.endswith(".txt"):
                reading_path = os.path.join(args.reading_path, file)
                details_path = os.path.join(args.details_dir, os.path.basename(args.reading_path))
                details = dg.create_details(reading_path, args.detail_count)
                dg.save_details(details, details_path)
    else:
        details_path = os.path.join(args.details_dir, os.path.basename(args.reading_path))
        details = dg.create_details(args.reading_path, args.detail_count)
        dg.save_details(details, f"{details_path}.json")
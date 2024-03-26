from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import StuffDocumentsChain, LLMChain, ReduceDocumentsChain
from langchain.chains.summarize import load_summarize_chain

import dotenv
import os
import argparse

dotenv.load_dotenv()

def generate_reading(topic, details):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", convert_system_message_to_human=True)
    db = Chroma(persist_directory=os.environ['CHROMA_PATH'], embedding_function=embeddings)
    llm = ChatGoogleGenerativeAI(model=os.environ['LLM_MODEL'], convert_system_message_to_human=True)
    
    detail_list = ', '.join(details)
    prompt_template = """You are an author who writes articles about cybersecurity.  
        You are given the following context: {text}.  Write an article specifically about the following topics: """ + detail_list + """.
        Each topic must contain 500 words. Go into detail about each topic.
        The introduction should only talk about the topics specified.
        """
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

    #chain = load_summarize_chain(llm,
    #                            chain_type="stuff",
    #                            prompt=prompt)

    documents = db.similarity_search(topic, k=25)
    document_prompt = PromptTemplate(
        input_variables=["page_content"],
        template="{page_content}"
    )
    document_variable_name = "context"
    # The prompt here should take as an input variable the
    # `document_variable_name`
    prompt = PromptTemplate.from_template(
        """You are an author who writes articles about cybersecurity.  
        You are given the following context: {context}.  Write an article specifically about the following topics: """ + detail_list + """.
        Each topic must contain 500 words. Go into detail about each topic.
        The introduction should only talk about the topics specified.
        """
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    combine_documents_chain = StuffDocumentsChain(
        llm_chain=llm_chain,
        document_prompt=document_prompt,
        document_variable_name=document_variable_name
    )
    chain = ReduceDocumentsChain(
        combine_documents_chain=combine_documents_chain,
    )

    return chain.run(documents)

if __name__ == '__main__':
    #topic = "password security"
    #details = ["strong passwords", "password managers", "password security", "recommended practices"]
    #reading = generate_reading(topic, details)
    #print(reading)
    parser = argparse.ArgumentParser(description='Generate reading')
    parser.add_argument('--topic', type=str, help='the topic of the reading', required=True)
    parser.add_argument('--details', nargs='+', help='the details of the reading', required=True)
    args = parser.parse_args()
    reading = generate_reading(args.topic, args.details)
    print(reading)
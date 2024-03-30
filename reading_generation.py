from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import StuffDocumentsChain, LLMChain, ReduceDocumentsChain
from langchain.chains.summarize import load_summarize_chain
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from multiprocessing import Pool


import dotenv
import os
import argparse

dotenv.load_dotenv()

def generate_reading(topic, details, difficulty):
    print(f"Generating reading for {topic} at {difficulty} difficulty")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", convert_system_message_to_human=True)
    db = Chroma(persist_directory=os.environ['CHROMA_PATH'], embedding_function=embeddings)
    llm = ChatGoogleGenerativeAI(model=os.environ['LLM_MODEL'], convert_system_message_to_human=True)
    
    detail_list = ', '.join(details)
    retriever = db.as_retriever()

    prompt = PromptTemplate.from_template(
        """You are an author who writes guides about cybersecurity topics.  The article is targeted at """ + difficulty + """ difficulty readers.
        Beginner readers are new to the topic and should be given a high level overview. Intermediate readers have some knowledge of the topic and need a more in-depth explanation. Expert readers are well versed in the topic and need a very detailed explanation.
        You are given the following context: {context}.  Write an article specifically about the following topics: """ + detail_list + """.
        Go in depth into every detail about the topics. The output MUST BE 10000 characters long.
        """
    )
    # The introduction should only talk about the topics specified. Write about each topic as much as you can.
    reading_chain = (
        {"context": retriever}
        | prompt
        | llm
        | StrOutputParser()
    )

    format_prompt = PromptTemplate.from_template(
        """You are given a document that contains the following text: {document}.
        It is written in markdown format.  Remove the markdown formatting.
        Remove any # headers. Remove any **bold** and *italic* text.  Replace and * bullets with -.
        Return the text as plain text.  These rules MUST be enforced.
        """
    )
    format_chain = (
        {"document": reading_chain}
        | format_prompt
        | llm 
        | StrOutputParser()
    )
    
    return format_chain.invoke(topic)

def save_reading(reading, save_path):
    with open(save_path, 'w') as f:
        f.write(reading)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate reading')
    parser.add_argument('--topic', type=str, help='the topic of the reading', required=True)
    parser.add_argument('--details', nargs='+', help='the details of the reading', required=True)
    parser.add_argument('--save_path', type=str, help='the directory to save the reading to', required=True)
    parser.add_argument('--name', type=str, help='the name of the reading file', required=True)
    parser.add_argument('--difficulty', nargs='+', help='the difficulty of the reading', required=False, default=['beginner', 'intermediate', 'expert'])
    args = parser.parse_args()

    reading_args = [(args.topic, args.details, difficulty) for difficulty in args.difficulty]
    readings = []
    with Pool() as p:
        readings = p.starmap(generate_reading, reading_args)
    
    for reading, difficulty in zip(readings, args.difficulty):
        save_reading(reading, f"{args.save_path}/{args.name}_{difficulty}.txt")
        print("Reading saved at", f"{args.save_path}/{args.name}_{difficulty}.txt") 

    # python reading_generation.py --topic "2fa" --details "introduction to topic" "what is 2fa" "2fa factors"  --save_path content_generation/content/reading/2fa --name introduction_to_2fa
    # 
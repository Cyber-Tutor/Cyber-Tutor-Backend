from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from multiprocessing import Pool

import dotenv
import os
import argparse

dotenv.load_dotenv()


"""
Generate reading content based on topic, details, and difficulty
Reading is generated, then formatting is refined
Returns reading content
"""
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
        Go in depth into every detail about the topics.  Replace any formatting with HTML tags.  Do not wrap then entire document in HTML tags.
        """
    )
    # chain to generate reading content
    reading_chain = (
        {"context": retriever}
        | prompt
        | llm
        | StrOutputParser()
    )

    format_prompt = PromptTemplate.from_template(
        """You are a HTML developer. You are given a document that contains the following text: {document}.
        You need to make it render inside an already prepared HTML document properly.  Replace the markdown formatting with HTML tags.
        Replace any **bold** text with <strong>bold</strong> text.  Replace any *italic* text with <em>italic</em> text.
        Replace any - lists with <ul> lists.  Replace any 1. lists with <ol> lists.
        Remove any duplicate tags. Do not include <!DOCTYPE html>, <html>, <head>, or <body> tags.
        Do not wrap the entire document with ```html``` tags.
        Make the title a <h1> tag.  Make the subtitles <h2> tags.  Make the paragraphs <p> tags.
        Make sure all tags are properly closed.
        """
    )
    # chain to format reading content
    format_chain = (
        {"document": reading_chain}
        | format_prompt
        | llm 
        | StrOutputParser()
    )
    
    return format_chain.invoke(topic)


"""
Save reading to file
"""
def save_reading(reading, save_path):
    with open(save_path, 'w') as f:
        f.write(reading)


if __name__ == '__main__':
    """
    Generate reading content based on topic and reading content
    Uses multiprocessing to generate readings for beginner, intermediate, and expert levels
    Reading is generated using content from the vector database and then formatted
    """
    parser = argparse.ArgumentParser(description='Generate reading')
    parser.add_argument('--topic', type=str, help='the topic of the reading', required=True)
    parser.add_argument('--details', nargs='+', help='the details of the reading', required=True)
    parser.add_argument('--save_path', type=str, help='the directory to save the reading to', required=True)
    parser.add_argument('--name', type=str, help='the name of the reading file')
    parser.add_argument('--difficulty', nargs='+', help='the difficulty of the reading', required=False, default=['beginner', 'intermediate', 'expert'])
    args = parser.parse_args()

    for difficulty in args.difficulty:
        if difficulty not in ['beginner', 'intermediate', 'expert']:
            raise ValueError("Invalid difficulty level.  Difficulty must be beginner, intermediate, or expert")
        
    # generate readings for each difficulty level using multiprocessing
    reading_args = [(args.topic, args.details, difficulty) for difficulty in args.difficulty]
    with Pool() as p:
        readings = p.starmap(generate_reading, reading_args)
    
    # save readings to file
    for reading, difficulty in zip(readings, args.difficulty):
        if not args.name:
            name = os.path.basename(os.path.normpath(args.save_path))
        else:
            name = args.name
        save_reading(reading, f"{args.save_path}/{name}_{difficulty}.txt")
        print("Reading saved at", f"{args.save_path}/{args.name}_{difficulty}.txt") 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import dotenv

import argparse
import os

from web_scraper import WebScraper

dotenv.load_dotenv()


"""
Load web page from url into chroma db
"""
def main(url_file):
    urls = read_file(url_file)
    docs = web_loader(urls)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", convert_system_message_to_human=True)
    db_path = os.environ['CHROMA_PATH']

    if os.path.exists(db_path):
        db = Chroma(persist_directory=db_path, embedding_function=embeddings)
        for doc in docs:
            db.add_documents(doc)
    else:
        db = Chroma.from_documents(docs[0], embeddings, persist_directory=db_path)
        for doc in docs[1:]:
            db.add_documents(doc)
    db.persist()


"""
Scrapes web pages from urls and returns split documents
"""
def web_loader(urls):
    documents = []
    for url in urls:
        print("Scraping: ", url)
        try: 
            # loads web page as documents
            loader = WebScraper(url)
            documents = loader.load()
            # splits documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=20)
            docs = text_splitter.split_documents(documents)
            print("docs: ", docs)
            if docs:
                documents.append(docs)
                print(docs)
        except:
            print("Failed to scrape: ", url)
            continue
    return documents


"""
Read urls from file
"""
def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.readlines()


if __name__ == '__main__':
    """
    Load web pages into chroma db from urls in a file
    """
    parser = argparse.ArgumentParser(description='Load web pages into chroma db')
    parser.add_argument('--urls', type=str, help='File name containing urls to load')
    
    args = parser.parse_args()
    main(args.urls)
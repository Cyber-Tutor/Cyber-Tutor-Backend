from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
import dotenv

import argparse
import os

dotenv.load_dotenv()


def main(url_file):
    urls = read_file(url_file)
    docs = web_loader(urls)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", convert_system_message_to_human=True)
    db_path = os.environ['CHROMA_PATH']

    if os.path.exists(db_path):
        db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    else:
        db = Chroma.from_documents(docs, embeddings, persist_directory=db_path)


def web_loader(urls):
    loader = WebBaseLoader(urls)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    return docs


def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.readlines()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load web pages into chroma db')
    parser.add_argument('urls', type=str, help='File name containing urls to load')
    
    args = parser.parse_args()
    main(args.urls)
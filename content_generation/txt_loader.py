from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
import argparse
import dotenv
import os

dotenv.load_dotenv()


"""
Load text from file into chroma db
"""
def main(file):
    loader = TextLoader(file)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", convert_system_message_to_human=True)
    db = Chroma(persist_directory=os.environ['CHROMA_PATH'], embedding_function=embeddings)
    db.add_documents(docs)
    db.persist()


if __name__ == '__main__':
    """
    Load text from file into chroma db
    """
    parser = argparse.ArgumentParser(description='Load text from file into chroma db')
    parser.add_argument('--content', type=str, help='the path to the content to store', required=True)
    args = parser.parse_args()

    main(args.content)
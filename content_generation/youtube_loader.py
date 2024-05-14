from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import os
import argparse


"""
Load transcript from a youtube video into Chroma db
"""
def main(args):
    loader = GenericLoader(
        YoutubeAudioLoader([args.url], args.save_dir),
        OpenAIWhisperParser()
    )
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", convert_system_message_to_human=True)
    db = Chroma(persist_directory=os.environ['CHROMA_PATH'], embedding_function=embeddings)
    db.add_documents(docs)
    db.persist()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load youtube transcripts into Chroma')
    parser.add_argument('--url', type=str, help='URL of youtube video to load')
    parser.add_argument('--save_dir', type=str, help='Directory to save youtube transcript')
    args = parser.parse_args()
    main(args)
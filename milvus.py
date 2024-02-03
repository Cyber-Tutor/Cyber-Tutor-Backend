from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Milvus
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings.openai import OpenAIEmbeddings
import os
import dotenv


dotenv.load_dotenv()

COLLECTION_NAME = 'cybertutor'

sources = [
    'https://authy.com/what-is-2fa/',
    'https://www.proofpoint.com/us/threat-reference/phishing',
    'https://www.beyondtrust.com/blog/entry/top-15-password-management-best-practices',
    'https://www.pcmag.com/how-to/12-simple-things-you-can-do-to-be-more-secure-online',
]

loader = WebBaseLoader([
    source for source in sources
])

docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
splits = text_splitter.split_documents(docs)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#embeddings = OpenAIEmbeddings()

connection_args = {'host': 'localhost', 'port': 19530}

vector_db = Milvus(
    embedding_function=embeddings,
    collection_name=COLLECTION_NAME,
    connection_args=connection_args,
    drop_old=True
).from_documents(
    splits, 
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    connection_args=connection_args)

query = "What is 2fa?"
docs = vector_db.similarity_search(query)

print(docs)

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.document_loaders import WebBaseLoader

from langchain.tools.retriever import create_retriever_tool
from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field


sources = [
    'https://authy.com/what-is-2fa/',
    'https://www.proofpoint.com/us/threat-reference/phishing',
    'https://www.beyondtrust.com/blog/entry/top-15-password-management-best-practices',
    'https://www.pcmag.com/how-to/12-simple-things-you-can-do-to-be-more-secure-online',
]

loader = WebBaseLoader([
    source for source in sources
])
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

print(len(texts))

for i, doc in enumerate(texts):
    doc.metadata["page_chunk"] = i

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

vectorstore = Chroma.from_documents(texts, embeddings, collection_name="cyber-tutor")
retriever = vectorstore.as_retriever()

retriever_tool = create_retriever_tool(
    retriever,
    "cyber-tutor-retriever",
    "Query a retriever to get information about cybersecurity related topics.",
)

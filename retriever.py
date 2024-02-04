from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains import RetrievalQA
import dotenv

dotenv.load_dotenv()

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

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", convert_system_message_to_human=True)

db = Chroma.from_documents(texts, embeddings, collection_name="cyber-tutor")
retriever = db.as_retriever()

db.persist()

llm = ChatGoogleGenerativeAI(model="models/gemini-pro", convert_system_message_to_human=True)

qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=retriever
)

question = "What is 2fa?"
result = qa_chain({"query": question})
print(result)
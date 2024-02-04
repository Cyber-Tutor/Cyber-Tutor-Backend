from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
import dotenv

dotenv.load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", convert_system_message_to_human=True)

db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = db.as_retriever()

llm = ChatGoogleGenerativeAI(model="models/gemini-pro", convert_system_message_to_human=True)

qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=retriever
)

question = "What is 2fa?"
result = qa_chain({"query": question})
print(result)
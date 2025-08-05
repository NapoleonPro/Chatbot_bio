import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

def create_vectorstore_from_pdf(pdf_path: str):
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=os.environ["GOOGLE_API_KEY"]
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_db")

    print("✅ Vector store berhasil dibuat dan disimpan.")

def load_vectorstore():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=os.environ["GOOGLE_API_KEY"]
    )
    return FAISS.load_local("faiss_db", embeddings, allow_dangerous_deserialization=True)

def retrieve_context(query: str, k=3):
    db = load_vectorstore()
    docs = db.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in docs])

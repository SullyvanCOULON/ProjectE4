"""import faiss
import numpy as np
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import pipeline

# Chargement et découpage des documents
def load_and_split_documents(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    return splitter.split_documents(documents)

# Création de l'embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Chargement des documents et génération des embeddings
documents = load_and_split_documents("/Users/sullyvancoulon/Desktop/ESIEE/E4-INF/Semestre 2/Projet E4/RAG/repport2024.pdf")
doc_texts = [doc.page_content for doc in documents]
doc_embeddings = embedding_model.embed_documents(doc_texts)

# Indexation des embeddings avec FAISS
dimension = len(doc_embeddings[0])
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(np.array(doc_embeddings, dtype=np.float32))
vectorstore = FAISS(embedding_function=embedding_model, index=faiss_index, docstore=doc_texts)

# Chargement du modèle LLM
llm_pipeline = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct")
llm = HuggingFacePipeline(pipeline=llm_pipeline)

# Création de la chaîne de récupération et génération
retriever = vectorstore.as_retriever()
qa_chain = RetrievalQA(llm=llm, retriever=retriever)

# Test de la RAG
query = "Quel genre est le plus responsable d'accidents de la route ?"
response = qa_chain.run(query)
print("Réponse générée:", response)"""
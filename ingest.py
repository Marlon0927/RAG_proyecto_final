import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

# Modelo embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection("documentos")

# Splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# Carpeta PDFs
docs_path = "./docs"

# Recorrer PDFs
for filename in os.listdir(docs_path):

    if filename.endswith(".pdf"):

        pdf_path = os.path.join(docs_path, filename)

        print(f"Procesando: {filename}")

        loader = PyPDFLoader(pdf_path)

        docs = loader.load()

        chunks = splitter.split_documents(docs)

        for i, chunk in enumerate(chunks):

            embedding = model.encode(chunk.page_content).tolist()

            collection.add(
                ids=[f"{filename}_{i}"],
                documents=[chunk.page_content],
                embeddings=[embedding],
                metadatas=[{
                    "source": filename,
                    "page": chunk.metadata.get("page", 0)
                }]
            )

print("✅ Base vectorial creada.")
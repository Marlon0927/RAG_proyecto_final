from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

# Modelo embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Leer PDF
#loader = PyPDFLoader("../docs/reglamento.pdf")
loader = PyPDFLoader("./docs/reglamento.pdf")
docs = loader.load()

# Dividir texto
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)

# ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection("reglamento")

# Guardar embeddings
for i, chunk in enumerate(chunks):

    embedding = model.encode(chunk.page_content)

    collection.add(
        ids=[str(i)],
        documents=[chunk.page_content],
        embeddings=[embedding.tolist()],
        metadatas=[{
            "page": chunk.metadata.get("page", 0)
        }]
    )

print("Base vectorial creada.")
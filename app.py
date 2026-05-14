import os
import shutil
import chromadb

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import UploadFile, File
from pydantic import BaseModel
from rag import consultar_rag
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


app = FastAPI()

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):

    # Crear carpeta docs
    os.makedirs("docs", exist_ok=True)

    pdf_path = f"docs/{file.filename}"

    # Guardar PDF
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Leer PDF
    loader = PyPDFLoader(pdf_path)

    docs = loader.load()

    # Dividir texto
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(
        docs
    )

    # ChromaDB
    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    # Eliminar colección vieja
    try:
        client.delete_collection(
            "reglamento"
        )
    except:
        pass

    collection = client.create_collection(
        "reglamento"
    )

    # Crear embeddings
    for i, chunk in enumerate(chunks):

        embedding = embedding_model.encode(
            chunk.page_content
        )

        collection.add(
            ids=[str(i)],
            documents=[
                chunk.page_content
            ],
            embeddings=[
                embedding.tolist()
            ],
            metadatas=[{
                "page":
                chunk.metadata.get(
                    "page",
                    0
                )
            }]
        )

    return {
        "message":
        f"PDF '{file.filename}' procesado correctamente"
    }

@app.post("/ask")
async def ask_question(
    data: QuestionRequest
):

    resultado = consultar_rag(
        data.question
    )

    return resultado
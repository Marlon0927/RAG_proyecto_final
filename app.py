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

# ========================================
# CONFIG
# ========================================

DOCS_PATH = "docs"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "documentos"

os.makedirs(DOCS_PATH, exist_ok=True)

# Modelo embeddings
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Chroma
client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    COLLECTION_NAME
)

# ========================================
# STATIC / TEMPLATES
# ========================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)

# ========================================
# MODELS
# ========================================

class QuestionRequest(BaseModel):
    question: str

# ========================================
# HOME
# ========================================

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

    try:

        print("\n========== UPLOAD PDF ==========")

        # Validar
        if not file.filename.endswith(".pdf"):

            print("❌ Archivo inválido")

            return {
                "message": "Solo PDFs"
            }

        print(f"📄 Archivo recibido: {file.filename}")

        # Ruta
        pdf_path = os.path.join(
            DOCS_PATH,
            file.filename
        )

        # Guardar PDF
        with open(pdf_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        print(f"✅ PDF guardado: {pdf_path}")

        # Leer PDF
        loader = PyPDFLoader(
            pdf_path
        )

        docs = loader.load()

        print(f"📚 Páginas cargadas: {len(docs)}")

        # Splitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(
            docs
        )

        print(f"✂️ Chunks generados: {len(chunks)}")

        # Guardar embeddings
        for i, chunk in enumerate(chunks):

            embedding = embedding_model.encode(
                chunk.page_content
            ).tolist()

            collection.add(

                ids=[
                    f"{file.filename}_{i}"
                ],

                documents=[
                    chunk.page_content
                ],

                embeddings=[
                    embedding
                ],

                metadatas=[{
                    "source": file.filename,
                    "page":
                    chunk.metadata.get(
                        "page",
                        0
                    )
                }]
            )

        print(f"✅ Embeddings guardados")

        print(
            "📦 Total colección:",
            collection.count()
        )

        print("========== FIN UPLOAD ==========\n")

        return {

            "message":
            f"PDF '{file.filename}' procesado correctamente",

            "chunks_count":
            len(chunks)
        }

    except Exception as e:

        print("❌ ERROR UPLOAD:")
        print(str(e))

        return {
            "message": str(e)
        }

# ========================================
# LISTAR PDFs
# ========================================

@app.get("/documents")
def get_documents():

    files = []

    for file in os.listdir(DOCS_PATH):

        if file.endswith(".pdf"):

            file_path = os.path.join(
                DOCS_PATH,
                file
            )

            files.append({

                "name": file,

                "size":
                round(
                    os.path.getsize(file_path) / 1024,
                    2
                )
            })

    return {
        "documents": files
    }

# ========================================
# ELIMINAR PDF
# ========================================

@app.delete("/documents/{filename}")
def delete_document(filename: str):

    pdf_path = os.path.join(
        DOCS_PATH,
        filename
    )

    # Eliminar archivo
    if os.path.exists(pdf_path):

        os.remove(pdf_path)

    # Buscar embeddings asociados
    results = collection.get()

    ids_to_delete = []

    for i, metadata in enumerate(
        results["metadatas"]
    ):

        if metadata.get("source") == filename:

            ids_to_delete.append(
                results["ids"][i]
            )

    # Eliminar embeddings
    if ids_to_delete:

        collection.delete(
            ids=ids_to_delete
        )

    return {
        "message":
        f"{filename} eliminado correctamente"
    }

# ========================================
# PREGUNTAS
# ========================================

@app.post("/ask")
async def ask_question(
    data: QuestionRequest
):

    resultado = consultar_rag(
        data.question
    )

    return resultado
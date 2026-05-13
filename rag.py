from sentence_transformers import SentenceTransformer
import chromadb
import google.generativeai as genai

from config import GEMINI_API_KEY

# Gemini
genai.configure(api_key=GEMINI_API_KEY)

gemini = genai.GenerativeModel(
    "gemini-2.0-flash"
)

# Embeddings
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ChromaDB
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    "reglamento"
)

def consultar_rag(pregunta):

    query_embedding = model.encode(pregunta)

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=3
    )

    documentos = results["documents"][0]

    contexto = "\n\n".join(documentos)

    prompt = f"""
Eres un asistente académico.

RESPONDE SOLO usando el contexto.

Si la respuesta no está en el contexto responde EXACTAMENTE:

"No encuentro esa información en el reglamento."

NO inventes información.
NO supongas artículos.

CONTEXTO:
{contexto}

PREGUNTA:
{pregunta}
"""

    response = gemini.generate_content(
        prompt
    )

    return {
        "respuesta": response.text,
        "fuentes": documentos
    }
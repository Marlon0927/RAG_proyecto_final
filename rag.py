from sentence_transformers import SentenceTransformer
import chromadb
import google.generativeai as genai

from config import GEMINI_API_KEY

# Configurar Gemini
genai.configure(
    api_key=GEMINI_API_KEY
)

gemini = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# Modelo embeddings
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def consultar_rag(pregunta):

    try:

        print("\n========== CONSULTA RAG ==========")

        print(f"❓ Pregunta: {pregunta}")

        # Conectar Chroma
        client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        collection = client.get_collection(
            "documentos"
        )

        print(
            "📦 Total embeddings:",
            collection.count()
        )

        # Embedding pregunta
        query_embedding = model.encode(
            pregunta
        ).tolist()

        print("✅ Embedding pregunta generado")

        # Buscar similares
        results = collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=3
        )

        print("🔎 RESULTADOS CHROMA:")
        print(results)

        documentos = results["documents"][0]

        # Validar documentos
        if not documentos:

            print("❌ Sin documentos encontrados")

            return {

                "respuesta":
                "No encontré información en los PDFs cargados.",

                "fuentes": []
            }

        print(
            f"📄 Documentos encontrados: {len(documentos)}"
        )

        for i, doc in enumerate(documentos):

            print(f"\n--- DOC {i+1} ---")
            print(doc[:300])

        contexto = "\n\n".join(
            documentos
        )

        print("\n🧠 CONTEXTO ENVIADO A GEMINI:")
        print(contexto[:1000])

        prompt = f"""
Eres un asistente académico.

RESPONDE SOLO usando el contexto segun el documento pdf analizado.

Si no encuentras la respuesta responde:

"No encuentro esa información."

CONTEXTO:
{contexto}

PREGUNTA:
{pregunta}
"""

        response = gemini.generate_content(
            prompt
        )

        print("\n✅ RESPUESTA GEMINI:")
        print(response.text)

        print("========== FIN CONSULTA ==========\n")

        return {

            "respuesta":
            response.text,

            "fuentes":
            documentos
        }

    except Exception as e:

        print("❌ ERROR RAG:")
        print(str(e))

        return {

            "respuesta":
            f"Error: {str(e)}",

            "fuentes": []
        }
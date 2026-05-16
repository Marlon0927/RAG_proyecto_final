from sentence_transformers import SentenceTransformer
import chromadb
import google.generativeai as genai

from config import GEMINI_API_KEY

from metrics import (
    evaluar_fidelidad,
    evaluar_relevancia,
    guardar_metricas
)

# ========================================
# GEMINI
# ========================================

genai.configure(
    api_key=GEMINI_API_KEY
)

gemini = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ========================================
# EMBEDDINGS
# ========================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ========================================
# CONSULTA RAG
# ========================================

def consultar_rag(pregunta):

    try:

        print("\n========== CONSULTA RAG ==========")

        print(f"❓ Pregunta: {pregunta}")

        # ========================================
        # CHROMA
        # ========================================

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

        # ========================================
        # EMBEDDING PREGUNTA
        # ========================================

        query_embedding = model.encode(
            pregunta
        ).tolist()

        print("✅ Embedding pregunta generado")

        # ========================================
        # BÚSQUEDA
        # ========================================

        results = collection.query(

            query_embeddings=[
                query_embedding
            ],

            n_results=3,

            include=[
                "documents",
                "distances",
                "metadatas"
            ]
        )

        documentos = results["documents"][0]

        distancias = results["distances"][0]

        print("🔎 RESULTADOS CHROMA:")
        print(results)

        # ========================================
        # VALIDACIÓN
        # ========================================

        if not documentos:

            print("❌ Sin documentos encontrados")

            return {

                "respuesta":
                "No encontré información en los PDFs cargados.",

                "fuentes": [],

                "fidelidad": 0,

                "relevancia": 0
            }

        print(
            f"📄 Documentos encontrados: {len(documentos)}"
        )

        for i, doc in enumerate(documentos):

            print(f"\n--- DOC {i+1} ---")
            print(doc[:300])

        # ========================================
        # CONTEXTO
        # ========================================

        contexto = "\n\n".join(
            documentos
        )

        print("\n🧠 CONTEXTO ENVIADO A GEMINI:")
        print(contexto[:1000])

        # ========================================
        # PROMPT
        # ========================================

        prompt = f"""
Eres un asistente académico.

RESPONDE SOLO usando el contexto según el documento PDF analizado.

Si no encuentras la respuesta responde:

"No encuentro esa información."

CONTEXTO:
{contexto}

PREGUNTA:
{pregunta}
"""

        # ========================================
        # GEMINI
        # ========================================

        response = gemini.generate_content(
            prompt
        )

        respuesta = response.text

        print("\n✅ RESPUESTA GEMINI:")
        print(respuesta)

        # ========================================
        # MÉTRICAS
        # ========================================

        fidelidad = evaluar_fidelidad(
            respuesta,
            contexto
        )

        relevancia = evaluar_relevancia(
            distancias
        )

        print(f"\n📊 Fidelidad: {fidelidad}")
        print(f"📊 Relevancia: {relevancia}")

        # ========================================
        # GUARDAR CSV
        # ========================================

        guardar_metricas({

            "pregunta": pregunta,

            "respuesta": respuesta,

            "fidelidad": fidelidad,

            "relevancia": relevancia
        })

        print("💾 Métricas guardadas")

        print("========== FIN CONSULTA ==========\n")

        # ========================================
        # RETORNO
        # ========================================

        return {

            "respuesta":
            respuesta,

            "fuentes":
            documentos,

            "fidelidad":
            fidelidad,

            "relevancia":
            relevancia
        }

    except Exception as e:

        print("❌ ERROR RAG:")
        print(str(e))

        return {

            "respuesta":
            f"Error: {str(e)}",

            "fuentes": [],

            "fidelidad": 0,

            "relevancia": 0
        }
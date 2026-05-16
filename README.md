# Asistente Académico IA — Sistema RAG con PDFs

<img width="1066" height="536" alt="image" src="https://github.com/user-attachments/assets/9bb016b3-f397-43aa-a44a-c789c4a2495b" />
---
<img width="949" height="506" alt="image" src="https://github.com/user-attachments/assets/f2067c4c-dbb5-48bd-956e-b345c6096870" />
---

## Descripción General

Este proyecto consiste en un sistema de inteligencia artificial basado en arquitectura RAG (Retrieval-Augmented Generation) capaz de analizar documentos PDF académicos mediante búsqueda semántica y generación de respuestas utilizando modelos de lenguaje.

La aplicación permite:

* Cargar múltiples documentos PDF.
* Procesar automáticamente el contenido textual.
* Dividir información en fragmentos semánticos.
* Generar embeddings vectoriales.
* Almacenar información en una base vectorial.
* Consultar documentos mediante lenguaje natural.
* Obtener respuestas contextualizadas usando Gemini.
* Visualizar documentos cargados desde una interfaz gráfica web.

---

# Objetivos del Proyecto

## Objetivo General

Desarrollar una aplicación inteligente basada en RAG que permita consultar documentos académicos mediante técnicas de búsqueda semántica e inteligencia artificial generativa.

## Objetivos Específicos

* Implementar un sistema de carga y procesamiento de PDFs.
* Construir una base vectorial utilizando embeddings semánticos.
* Integrar modelos de IA generativa para responder preguntas.
* Diseñar una interfaz gráfica amigable para interacción usuario-documento.
* Permitir administración dinámica de documentos.

---

# Arquitectura de la Solución

La solución implementa una arquitectura RAG compuesta por:

1. Frontend Web.
2. Backend API.
3. Motor de embeddings.
4. Base de datos vectorial.
5. Modelo generativo.
6. Sistema de recuperación semántica.

## Arquitectura General

```text
Usuario
   │
   ▼
Frontend (HTML + CSS + JavaScript)
   │
   ▼
FastAPI Backend
   │
   ├── Upload PDF
   ├── Procesamiento de texto
   ├── Chunking
   ├── Embeddings
   ├── Consulta semántica
   │
   ▼
ChromaDB (Base Vectorial)
   │
   ▼
Gemini API
   │
   ▼
Respuesta Inteligente
```

---

# Tecnologías Utilizadas

| Tecnología           | Descripción              |
| -------------------- | ------------------------ |
| Python               | Lenguaje principal       |
| FastAPI              | Backend API              |
| ChromaDB             | Base de datos vectorial  |
| SentenceTransformers | Generación de embeddings |
| Gemini 2.5 Flash     | Modelo generativo        |
| HTML/CSS/JavaScript  | Interfaz gráfica         |
| PyPDFLoader          | Lectura de PDFs          |
| LangChain            | Procesamiento documental |

---

# Estructura del Proyecto

```text
proyecto-rag/
│
├── app.py
├── rag.py
├── config.py
├── requirements.txt
│
├── chroma_db/
├── docs/
│
├── templates/
│   └── index.html
│
├── static/
│   ├── styles.css
│   └── script.js
│
└── README.md
```

---

# Flujo General del Sistema

## 1. Carga del Documento

El usuario selecciona un archivo PDF desde la interfaz gráfica.

El frontend envía el archivo mediante una petición POST hacia:

```text
/upload-pdf
```

---

## 2. Ingesta del Documento

El backend:

* Guarda el PDF.
* Extrae texto.
* Divide contenido.
* Genera embeddings.
* Almacena vectores.

### Código principal de ingesta

```python
loader = PyPDFLoader(pdf_path)
docs = loader.load()
```

---

# Proceso de Chunking

El documento es dividido en fragmentos pequeños llamados chunks.

Esto mejora:

* Recuperación semántica.
* Precisión contextual.
* Rendimiento del modelo.

## Configuración utilizada

```python
RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
```

## Explicación

| Parámetro     | Función                        |
| ------------- | ------------------------------ |
| chunk_size    | Tamaño máximo del fragmento    |
| chunk_overlap | Superposición entre fragmentos |

---

# Vectorización del Documento

Cada chunk se transforma en un embedding semántico.

## Modelo utilizado

```python
all-MiniLM-L6-v2
```

## Generación del embedding

```python
embedding = embedding_model.encode(
    chunk.page_content
).tolist()
```

Los embeddings representan matemáticamente el significado semántico del texto.

---

# Base Vectorial

Se utiliza ChromaDB como motor de almacenamiento vectorial.

## Funciones principales

* Almacenar embeddings.
* Realizar búsquedas semánticas.
* Recuperar contexto relevante.

## Inserción de datos

```python
collection.add(
    ids=[f"{file.filename}_{i}"],
    documents=[chunk.page_content],
    embeddings=[embedding]
)
```

---

# Flujo de Consulta RAG

Cuando el usuario realiza una pregunta:

1. La pregunta se convierte en embedding.
2. Chroma busca chunks similares.
3. Se construye contexto.
4. Gemini genera respuesta.

---

# Construcción del Prompt Aumentado

El sistema utiliza Prompt Engineering para limitar respuestas únicamente al contexto recuperado.

## Prompt implementado

```text
Eres un asistente académico.

RESPONDE SOLO usando el contexto.

Si no encuentras la respuesta responde:

"No encuentro esa información."

NO inventes información.
```

## Objetivo del Prompt

* Reducir alucinaciones.
* Mejorar precisión.
* Responder únicamente con evidencia documental.

---

# Recuperación Semántica

La búsqueda se realiza mediante similitud vectorial.

## Consulta implementada

```python
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)
```

## Funcionamiento

El sistema compara:

* embedding de la pregunta
  contra
* embeddings de los documentos

para encontrar información relacionada semánticamente.

---

# Interfaz Gráfica (GUI)

La aplicación cuenta con una interfaz web moderna que permite:

* Subir PDFs.
* Visualizar documentos cargados.
* Eliminar documentos.
* Realizar preguntas.
* Ver respuestas y fuentes.

## Componentes principales

### Gestión de documentos

* Lista dinámica de PDFs.
* Estado de carga.
* Eliminación de archivos.

### Área de consultas

* Campo de preguntas.
* Visualización de respuestas.
* Visualización de fuentes recuperadas.

---

# Manejo de Documentos

El sistema soporta:
D
* Persistencia de embeddings.
* Eliminación dinámica.
* Reindexación automática.

---

# Resultados Obtenidos

## Resultados Funcionales

El sistema logró:

* Procesar correctamente documentos PDF.
* Generar embeddings semánticos.
* Recuperar contexto relevante.
* Generar respuestas contextualizadas.
* Integrar IA generativa con búsqueda semántica.

## Resultados Técnicos

| Funcionalidad      | Estado   |
| ------------------ | -------- |
| Upload PDF         | Correcto |
| Chunking           | Correcto |
| Embeddings         | Correcto |
| ChromaDB           | Correcto |
| Consulta semántica | Correcto |
| Generación IA      | Correcto |

---

# Problemas Encontrados

Durante el desarrollo se identificaron desafíos como:

* Manejo incorrecto de tensores.
* Persistencia de embeddings antiguos.
* Recuperación de PDFs eliminados.
* Configuración de embeddings incompatibles.
* Gestión de múltiples documentos.

## Soluciones Aplicadas

* Conversión de embeddings a listas.
* Reestructuración de ChromaDB.
* Uso de IDs únicos.
* Limpieza de colecciones antiguas.
* Implementación de logs de depuración.

---

# Seguridad y Validaciones

El sistema incluye:

* Validación de tipo PDF.
* Manejo de errores.
* Restricción de respuestas fuera de contexto.
* Manejo seguro de archivos.

---

# Posibles Mejoras Futuras

## Mejoras Técnicas

* OCR para PDFs escaneados.
* Streaming de respuestas.
* Memoria conversacional.
* Autenticación de usuarios.
* Dockerización.
* Despliegue cloud.
* Soporte para Word y Excel.

## Mejoras IA

* Reranking.
* Hybrid Search.
* Fine-Tuning.
* Agentes inteligentes.
* Citación exacta por página.

---

# Conclusiones

El proyecto demuestra la integración efectiva entre búsqueda semántica y modelos generativos mediante arquitectura RAG.

La solución permite transformar documentos académicos en una fuente consultable mediante lenguaje natural, facilitando el acceso a la información y automatizando procesos de consulta documental.

El sistema logró implementar exitosamente:

* procesamiento documental,
* vectorización semántica,
* recuperación contextual,
* generación de respuestas inteligentes,
* y administración dinámica de múltiples documentos.

---

# Requisitos de Instalación

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecutar aplicación

```bash
uvicorn app:app --reload
```

---

# Variables de Entorno

Archivo:

```text
config.py
```

## Configuración requerida

```python
GEMINI_API_KEY = "TU_API_KEY"
```

---


# 🎓 SaySo-RAG | Thapar University AI Assistant

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![RAG](https://img.shields.io/badge/Architecture-RAG-7C3AED)](#how-it-works)
[![Embeddings](https://img.shields.io/badge/Embeddings-BGE--small--en--v1.5-0A66C2)](https://huggingface.co/BAAI/bge-small-en-v1.5)
[![Vector Search](https://img.shields.io/badge/Vector%20Search-FAISS-00A98F)](https://github.com/facebookresearch/faiss)
[![LLM](https://img.shields.io/badge/LLM-Llama%203.2%203B-111827)](https://ollama.com/library/llama3.2)
[![Local Inference](https://img.shields.io/badge/Inference-Ollama-black?logo=ollama)](https://ollama.com/)
[![API](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![UI](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

**SaySo-RAG** is a Retrieval-Augmented Generation (RAG) assistant for students of **Thapar Institute of Engineering & Technology (TIET)**. It retrieves relevant information from publicly available university web pages and official PDF documents, then uses a language model to produce a grounded, conversational answer with source references.

> The project is intended to make university information easier to find. For important or time-sensitive decisions, always verify details with the relevant university department or the latest official notice.

---

## ✨ Features

- **University-focused knowledge base:** collects public pages and PDF documents from Thapar's website.
- **Document processing pipeline:** extracts, cleans, and splits web/PDF content into searchable chunks.
- **Semantic retrieval:** creates dense embeddings and searches them using FAISS.
- **Grounded answer generation:** passes retrieved context to a locally served Llama model through Ollama.
- **Source references:** returns source links and short previews alongside answers.
- **Two ways to use it:** Streamlit chat interface and a FastAPI endpoint.
- **Basic input guardrails:** handles greetings, thanks, goodbyes, and very short inputs without running retrieval.

## 🧰 Tech Stack

| Area | Technology | Purpose |
|---|---|---|
| Language | Python | Application and data pipeline |
| Web scraping | Requests, Beautiful Soup, lxml | Discover and extract public university web content |
| PDF processing | pypdf | Extract text from PDF documents |
| Text processing | Python utilities, LangChain packages | Clean and split source content |
| Embeddings | Sentence Transformers, `BAAI/bge-small-en-v1.5` | Convert chunks and user questions into 384-dimensional vectors |
| Vector search | FAISS (`faiss-cpu`) | Store and search the dense vector index |
| LLM serving | Ollama | Run the language model locally |
| Language model | Llama 3.2 3B | Generate answers from retrieved context |
| RAG orchestration | Python | Connect retrieval, prompt construction, and generation |
| Web interface | Streamlit | Interactive chat UI |
| API | FastAPI, Uvicorn | Expose the RAG pipeline through HTTP |

### Technology tags

`Python` `RAG` `Semantic Search` `Sentence Transformers` `BGE` `FAISS` `Vector Index` `Ollama` `Llama 3.2` `FastAPI` `Streamlit` `Beautiful Soup` `PDF Extraction`

---

## 🧠 How It Works

SaySo-RAG has two main stages: an **offline ingestion and indexing pipeline**, followed by an **online question-answering pipeline**.

### 1. Data ingestion and indexing

```text
Thapar University website + official PDFs
                  |
                  v
       Sitemap and URL discovery
                  |
                  v
          URL filtering
                  |
                  v
      Web-page scraping + PDF download
                  |
                  v
       PDF text extraction + cleaning
                  |
                  v
          Text chunking
                  |
                  v
     BGE embedding generation
                  |
                  v
       FAISS index + metadata
```

The current chunking configuration uses a target chunk size of **1,200 characters**, an overlap of **200 characters**, and a minimum chunk size of **200 characters**.

### 2. Question answering

```text
             Student question
                    |
                    v
              Input guardrails
                    |
                    v
       BGE query embedding (384 dimensions)
                    |
                    v
          FAISS similarity search
                    |
                    v
       Top 8 chunks (score threshold 0.30)
                    |
                    v
       Context + question prompt
                    |
                    v
          Ollama / Llama 3.2 3B
                    |
                    v
       Answer + source references
```

The query embedding is normalized before search. The FAISS index uses `IndexFlatIP`; because the vectors are normalized, inner-product ranking is equivalent to cosine-similarity ranking.

## 🗂️ Project Structure

```text
SaySo-RAG/
├── scrape/
│   ├── 01_download_sitemap.py
│   ├── 02_parse_urls.py
│   ├── 03_filter_urls.py
│   ├── 04_scrape_pages.py
│   └── 05_download_pdfs.py
│
├── src/
│   ├── 00_build_pdf_url_map.py
│   ├── 01_extract_pdfs.py
│   ├── 02_clean_data.py
│   ├── 03_chunk_data.py
│   ├── 04_build_index.py
│   ├── 05_rag_chain.py
│   ├── 06_app.py
│   ├── api_server.py
│   ├── rag_chain_utils.py
│   └── source_utils.py
│
├── data/
│   ├── sitemap/
│   ├── raw/
│   ├── processed/
│   └── chunks/
│
├── index/
│   ├── faiss_index/
│   │   └── index.faiss
│   └── chunks_metadata.jsonl
│
├── requirement.txt
└── README.md
```

Generated data and index files may not be present in a fresh clone. Run the ingestion pipeline to create them.

---

## ⚙️ Getting Started

### Prerequisites

Install the following before running the project:

- Python and pip
- [Ollama](https://ollama.com/download)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/SayySoo/SaySo-RAG.git
cd SaySo-RAG
```

### 2. Install Python dependencies

The repository's dependency file is named `requirement.txt` (singular):

```bash
pip install -r requirement.txt
```

The current application imports a few packages that may not yet be listed in that file. Install these as well if they are missing:

```bash
pip install langchain-ollama python-dotenv fastapi uvicorn
```

### 3. Download the local language model

Start Ollama, then pull the model used by the shared Streamlit/FastAPI RAG pipeline:

```bash
ollama pull llama3.2:3b
```

Make sure the Ollama service is running before asking the assistant a question.

### 4. Build the knowledge base

Run the scripts from the repository root, in order:

```bash
# Discover and filter university pages
python scrape/01_download_sitemap.py
python scrape/02_parse_urls.py
python scrape/03_filter_urls.py

# Scrape pages and download linked PDFs
python scrape/04_scrape_pages.py
python scrape/05_download_pdfs.py

# Extract, clean, and chunk the source content
python src/00_build_pdf_url_map.py
python src/01_extract_pdfs.py
python src/02_clean_data.py
python src/03_chunk_data.py

# Generate embeddings and build the FAISS index
python src/04_build_index.py
```

The index-building step creates:

- `index/faiss_index/index.faiss`: the FAISS vector index.
- `index/chunks_metadata.jsonl`: chunk text and its associated source metadata.

**Important:** keep the FAISS index and metadata file from the same build together. FAISS search results return positional indices, and the application uses those positions to look up the corresponding metadata entries.

### 5. Run the Streamlit application

From the project root:

```bash
streamlit run src/06_app.py
```

### 6. Run the FastAPI server (alternative interface)

```bash
python -m src.api_server
```

The API runs on port **8001** by default.

**Endpoint:** `POST /chat`

Example request:

```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Where can I find information about hostel rules?"}'
```

The response includes a status, generated answer, and source information.

---

## 🔎 Vector Search: FAISS

This project uses **FAISS as its vector indexing and similarity-search engine**. It is not a managed, full-featured vector database service.

- **Embedding model:** `BAAI/bge-small-en-v1.5`
- **Vector dimension:** 384
- **Index type:** `faiss.IndexFlatIP`
- **Similarity:** inner product over normalized embeddings (equivalent to cosine similarity)
- **Retrieval count:** top 8 results by default
- **Minimum score:** 0.30

Key implementation files:

| File | Responsibility |
|---|---|
| `src/04_build_index.py` | Generates embeddings and writes the FAISS index and metadata |
| `src/rag_chain_utils.py` | Loads the index, embeds questions, retrieves chunks, and generates answers |
| `index/faiss_index/index.faiss` | Persisted FAISS index |
| `index/chunks_metadata.jsonl` | Text chunks and source metadata aligned with FAISS positions |

---

## 🧪 Testing

A retrieval smoke-test script is available:

```bash
python src/test_retrieval.py
```

Use questions whose answers can be checked against the original university sources. Also test unrelated questions to verify that the system handles missing context appropriately.

## ⚠️ Current Scope and Limitations

- Answers depend on the content collected during the last ingestion run; the knowledge base is not automatically refreshed.
- Retrieval quality depends on source quality, chunk boundaries, the embedding model, and the retrieval threshold.
- The current FAISS `IndexFlatIP` performs exact similarity search. It is straightforward to use, but search cost grows with the number of indexed vectors.
- The assistant can still produce incorrect or incomplete answers. Retrieved context and prompt instructions reduce this risk but do not eliminate it.
- The current shared application pipeline uses **Ollama with Llama 3.2 3B**. The separate `src/05_rag_chain.py` script is an alternate/standalone chain and should not be confused with the Streamlit/FastAPI runtime path.
- `rank-bm25` is present in the dependency list, but the current shared retrieval function uses FAISS; it does not currently perform hybrid BM25 + vector search.

## 🚀 Possible Future Improvements

- Add scheduled or incremental crawling to keep university information fresh.
- Evaluate retrieval with Recall@K, Precision@K, and MRR using a curated question set.
- Evaluate answer faithfulness and correctness against official source material.
- Experiment with reranking and hybrid keyword + vector retrieval.
- Add document-level filters and richer metadata.
- Add authentication, rate limiting, and restrictive CORS settings before exposing the API publicly.
- Compare local language models and tune generation settings based on evaluation results.

---

## 📄 Disclaimer

SaySo-RAG is an educational/student project and is not an official Thapar Institute service. It is not affiliated with or endorsed by Thapar Institute of Engineering & Technology. Always consult the latest official university communication for authoritative information.

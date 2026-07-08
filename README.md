# SAP-RAG-Assistant

# SAP BTP Knowledge Assistant (RAG)

A lightweight **Retrieval-Augmented Generation (RAG)** application built using **Python**, **TF-IDF**, and **Groq LLM** to answer SAP BTP-related questions from a custom knowledge base.

Instead of relying solely on an LLM's pre-trained knowledge, this project retrieves the most relevant information from local SAP BTP documentation and then uses a Large Language Model (LLM) to generate accurate, context-aware responses.

---

# Features

- Retrieval-Augmented Generation (RAG)
- Local knowledge base using `.txt` documents
- TF-IDF based document retrieval
- Cosine Similarity search
- Groq LLM integration
- Environment variable support using `.env`
- Modular and easy-to-understand architecture
- Easily extendable to embeddings and vector databases

---

# Architecture

```
                User Question
                       │
                       ▼
          TF-IDF Retriever
                       │
      Searches Local Documents
                       │
                       ▼
      Retrieves Top K Chunks
                       │
                       ▼
            Prompt Builder
                       │
 Adds Retrieved Context to Prompt
                       │
                       ▼
             Groq LLM API
                       │
                       ▼
         Natural Language Answer
```

---

# Project Structure

```
sap-rag-assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── docs/
│   ├── ai_core_genai_hub.txt
│   ├── cds_views.txt
│   ├── rap_model.txt
│   ├── sap_joule.txt
│   ├── ...
│
└── .venv/
```

---

# Technologies Used

- Python 3.12+
- Groq API
- Groq SDK
- Scikit-Learn
- TF-IDF Vectorizer
- Cosine Similarity
- python-dotenv

---

# How It Works

## Step 1 — Index Documents

The application reads every `.txt` document inside the `docs` folder.

Example:

```
docs/
    ai_core_genai_hub.txt
    cds_views.txt
    rap_model.txt
```

Each document is split into paragraph-level chunks.

Example:

```
Paragraph 1

Paragraph 2

Paragraph 3
```

Each paragraph becomes an individual searchable chunk.

---

## Step 2 — Build the Search Index

The application converts every paragraph into numerical vectors using:

```
TfidfVectorizer()
```

TF-IDF measures how important each word is inside every document.

---

## Step 3 — User asks a Question

Example

```
What is RAP?
```

---

## Step 4 — Retrieve Relevant Chunks

The retriever compares the question against every paragraph using:

- TF-IDF
- Cosine Similarity

Example:

```
rap_model.txt     0.343
rap_model.txt     0.288
cds_views.txt     0.146
```

Only the Top-K most relevant chunks are selected.

---

## Step 5 — Prompt Augmentation

The retrieved paragraphs are inserted into a prompt.

Example

```
CONTEXT

[Source: rap_model.txt]

RAP stands for RESTful Application Programming Model...

QUESTION

What is RAP?
```

---

## Step 6 — Generation

The prompt is sent to Groq.

The LLM does **NOT** search your documents.

Instead, it:

- Reads the retrieved context
- Understands it
- Generates a natural-language answer

This prevents hallucinations and keeps answers grounded in your knowledge base.

---

# Why Use RAG?

Without RAG

```
Question
      │
      ▼
      LLM
      │
      ▼
Answer
```

The model answers using only its pre-trained knowledge.

---

With RAG

```
Question
      │
      ▼
Retriever
      │
      ▼
Knowledge Base
      │
      ▼
Relevant Context
      │
      ▼
LLM
      │
      ▼
Answer
```

The answer is based on your own documents.

---

# Knowledge Base

Current topics include:

- SAP RAP
- SAP CDS Views
- SAP Joule
- SAP AI Core
- SAP Generative AI Hub

Adding more knowledge is simple.

Just place additional `.txt` files inside:

```
docs/
```

No code changes are required.

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/<your-username>/sap-rag-assistant.git

cd sap-rag-assistant
```

---

## Create a Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate

PowerShell

```bash
.venv\Scripts\Activate.ps1
```

Command Prompt

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Create a .env File

Create a file named

```
.env
```

Add

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
TOP_K=3
```

---

# Run the Application

```bash
python app.py
```

---

# Example

```
> What is RAP?
```

Output

```
Retrieved Sources

• rap_model.txt
• rap_model.txt
• cds_views.txt

Generating Answer...

RAP (RESTful Application Programming Model) is SAP's modern programming model for developing cloud-ready business applications...
```

---

# Configuration

Configuration is managed through `.env`.

| Variable | Description |
|-----------|-------------|
| GROQ_API_KEY | Your Groq API Key |
| GROQ_MODEL | LLM Model |
| TOP_K | Number of retrieved chunks |

---

# Dependencies

```
groq
python-dotenv
scikit-learn
```

---

# Future Improvements

This project currently uses **TF-IDF** retrieval.

Future enhancements include:

- Sentence Transformers
- HuggingFace Embeddings
- FAISS Vector Database
- SAP HANA Cloud Vector Engine
- ChromaDB
- LangChain
- Hybrid Search
- Metadata Filtering
- Document Upload UI
- Streamlit Web Application
- Chat Memory
- Multi-turn Conversations
- PDF Support
- DOCX Support

---

# Screenshots

## Terminal

(Add Screenshot Here)

---

## Retrieval Output

(Add Screenshot Here)

---

## Generated Answer

(Add Screenshot Here)

---

# Skills Demonstrated

- Retrieval-Augmented Generation (RAG)
- Prompt Engineering
- Information Retrieval
- TF-IDF
- Cosine Similarity
- Large Language Models
- Groq API
- Python
- Environment Variables
- Software Architecture
- Modular Programming

---

# Learning Outcome

This project demonstrates how a Retrieval-Augmented Generation pipeline works without requiring expensive embedding models or vector databases.

It clearly separates:

- Retrieval
- Prompt Augmentation
- Generation

making it an excellent foundation for building production-grade AI assistants.

---

# Author

**Mohammed Kaifulla Kazim**

Associate Consultant – SAP

LinkedIn: https://www.linkedin.com/in/mohammed-kaifulla/

---

# License

This project is released under the MIT License.

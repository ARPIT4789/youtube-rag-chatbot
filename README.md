# Multilingual YouTube AI Tutor (RAG)

An AI-powered chatbot that allows users to interact with YouTube videos by asking questions, generating structured notes, and exporting them as PDF files.  
The system uses **Retrieval Augmented Generation (RAG)** to ensure accurate, context-aware answers.

---

## Features

-  Accepts YouTube video links
-  Uses RAG for accurate question answering
-  Multilingual support (English, Hindi, Hinglish)
-  Generates structured study notes
-  Exports notes as PDF
-  Clean and interactive Streamlit UI
-  Uses **local embeddings** (no embedding API cost)

---

## Tech Stack

- **Python**
- **Streamlit** – Frontend
- **LangChain** – RAG framework
- **FAISS** – Vector database
- **Sentence Transformers (MiniLM)** – Local embeddings
- **Google Gemini API** – LLM for reasoning
- **YouTube Transcript API**
- **ReportLab** – PDF generation


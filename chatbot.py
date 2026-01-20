from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

def load_qa_chain():

    embeddings = HuggingFaceEmbeddings(
         model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
  


    if not os.path.exists("faiss_index"):
        raise FileNotFoundError("FAISS index not found. Please process a video first.")

    vector_store = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )


    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2
    )

    prompt = PromptTemplate.from_template("""
You are an AI YouTube tutor.

You MUST strictly follow this rule:

- If the question is in English → answer ONLY in English.
- If the question is in Hindi → answer ONLY in Hindi.
- If the question is in Hinglish → answer ONLY in Hinglish.

Do NOT translate unless the user asks.
Do NOT mix languages.

Use ONLY the given context to answer.

Context:
{context}

Question:
{input}

Answer clearly in structured study notes format.
""")


    document_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=prompt
    )

    retrieval_chain = create_retrieval_chain(
        retriever,
        document_chain
    )

    return retrieval_chain

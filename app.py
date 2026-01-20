import streamlit as st
import os
from ingest import ingest
from chatbot import load_qa_chain
from pdf_export import generate_pdf_bytes

st.set_page_config(page_title="YouTube Multilingual Chatbot", layout="wide")

st.title("YouTube Multilingual AI Tutor")

# Sidebar
with st.sidebar:
    st.header("Add YouTube Video")
    video_url = st.text_input("YouTube URL")
    process_btn = st.button("Process Video")

if process_btn and video_url:
    with st.spinner("Processing video..."):
        ingest(video_url)
    st.success("Video processed successfully! Ask questions now.")

# Load RAG chain
qa_chain = None

if os.path.exists("faiss_index"):
    try:
        qa_chain = load_qa_chain()
    except Exception as e:
        st.error("Failed to load knowledge base. Please reprocess the video.")


# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if qa_chain is None:
    st.info("👆 Please add and process a YouTube video first.")
    st.stop()

user_question = st.chat_input("Ask something about the video...")


if user_question:
    st.session_state.messages.append(
        {"role": "user", "content": user_question}
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = qa_chain.invoke({"input": user_question})
            answer = response["answer"]


        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

st.divider()

# PDF Export

if st.button("📄 Export Notes as PDF"):
    pdf_buffer = generate_pdf_bytes(st.session_state.messages)

    st.download_button(
        label="⬇️ Download PDF",
        data=pdf_buffer,
        file_name="youtube_notes.pdf",
        mime="application/pdf"
    )

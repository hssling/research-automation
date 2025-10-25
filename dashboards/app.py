import os, glob, fitz
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from transformers import pipeline

st.set_page_config(page_title="AI Research Assistant", layout="wide")
st.title("🧠 Automated Research Dashboard")

# === Summarization + RAG Load ===
hf_pipe = pipeline("summarization", model="facebook/bart-large-cnn")
llm = HuggingFacePipeline(pipeline=hf_pipe)
emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="./indexes", embedding_function=emb)
retriever = db.as_retriever(search_kwargs={"k":3})
prompt = PromptTemplate.from_template("Answer based on documents:\n{context}\n\nQuestion:{question}")
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type_kwargs={"prompt":prompt})

# === Sidebar Upload ===
with st.sidebar:
    st.header("📁 Upload new PDFs")
    uploaded = st.file_uploader("Upload PDF(s)", accept_multiple_files=True, type=["pdf"])
    if uploaded:
        os.makedirs("./data/pdfs", exist_ok=True)
        for f in uploaded:
            path = os.path.join("./data/pdfs", f.name)
            open(path, "wb").write(f.read())
        st.success("✅ Uploaded successfully. Run pipeline to refresh index.")

# === Query Interface ===
query = st.text_input("Ask a question about your research papers:")
if st.button("Submit") and query.strip():
    with st.spinner("Thinking..."):
        ans = qa.run(query)
        st.write("### 🤖 Answer:")
        st.write(ans)

# === View Summaries ===
st.markdown("---")
st.header("📄 Summarized Documents")
summaries = glob.glob("./data/processed/*.txt")
for s in summaries:
    with open(s, encoding="utf-8") as f:
        st.subheader(os.path.basename(s))
        st.write(f.read())

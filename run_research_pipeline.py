"""
Automated Research Platform
----------------------------
1️⃣ Extract PDFs → text
2️⃣ Summarize using Hugging Face LLM
3️⃣ Build RAG index (Chroma)
4️⃣ Push results to GitHub
"""

import os, glob, fitz
from datetime import datetime
from langchain_community.llms import HuggingFacePipeline
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from transformers import pipeline
from git import Repo

# === PDF → TEXT ===
def extract_pdfs(pdf_dir="./data/pdfs", out_dir="./data/raw"):
    os.makedirs(out_dir, exist_ok=True)
    for pdf in glob.glob(f"{pdf_dir}/*.pdf"):
        name = os.path.basename(pdf).replace(".pdf", ".txt")
        out_path = os.path.join(out_dir, name)
        if not os.path.exists(out_path):
            with fitz.open(pdf) as doc:
                text = "".join(page.get_text() for page in doc)
            open(out_path, "w", encoding="utf-8").write(text)
            print(f"📄 Extracted: {name}")

# === SUMMARIZATION ===
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
llm = HuggingFacePipeline(pipeline=summarizer)

def summarize_folder(in_dir="./data/raw", out_dir="./data/processed"):
    os.makedirs(out_dir, exist_ok=True)
    for file in glob.glob(f"{in_dir}/*.txt"):
        text = open(file, encoding="utf-8").read()[:3000]
        summary = llm(text)[0]['summary_text']
        out_path = os.path.join(out_dir, "summary_" + os.path.basename(file))
        open(out_path, "w", encoding="utf-8").write(summary)
        print(f"✅ Summarized: {file}")

# === RAG INDEX ===
def build_index(src="./data/processed", idx="./indexes"):
    os.makedirs(idx, exist_ok=True)
    docs = [open(f, encoding="utf-8").read() for f in glob.glob(f"{src}/*.txt")]
    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Chroma.from_texts(docs, embedding=emb, persist_directory=idx)
    print("🔍 Index built and saved.")

# === QUERY TEST ===
def query_index(q, idx="./indexes"):
    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma(persist_directory=idx, embedding_function=emb)
    retriever = db.as_retriever(search_kwargs={"k":3})
    prompt = PromptTemplate.from_template("Answer concisely from context:\n{context}\n\nQuestion:{question}")
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type_kwargs={"prompt":prompt})
    print("🤖", qa.run(q))

# === GITHUB PUSH ===
def auto_commit():
    try:
        repo = Repo(".")
        repo.git.add(A=True)
        repo.index.commit(f"Auto update: {datetime.now()}")
        repo.git.push("origin","main")
        print("🚀 Results pushed to GitHub.")
    except Exception as e:
        print("⚠️ Push failed:", e)

if __name__ == "__main__":
    extract_pdfs()
    summarize_folder()
    build_index()
    query_index("Summarize recent TB outcome findings.")
    auto_commit()

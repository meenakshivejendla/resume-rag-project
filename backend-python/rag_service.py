from fastapi import FastAPI
from parser import parse_pdf

from sentence_transformers import SentenceTransformer
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter

app = FastAPI()

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.create_collection("resume")

@app.post("/process")
def process(data: dict):

    resume_path = data["resume"]
    jd_path = data["jd"]

    resume_text = parse_pdf(resume_path)
    jd_text = parse_pdf(jd_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(resume_text)

    embeddings = model.encode(chunks)

    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=[str(i) for i in range(len(chunks))]
    )

    jd_skills = ["react","node","aws","postgres"]

    matches = [
        skill for skill in jd_skills
        if skill in resume_text.lower()
    ]

    score = int(len(matches)/len(jd_skills)*100)

    return {
        "match_score": score,
        "strengths": matches,
        "gaps": list(set(jd_skills)-set(matches))
    }


@app.post("/chat")
def chat(data: dict):

    question = data["question"]

    query_embedding = model.encode([question])

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=3
    )

    context = " ".join(results["documents"][0])

    return {
        "answer": f"Based on resume: {context[:300]}"
    }
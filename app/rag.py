import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_docs():
    docs = []
    filenames = []

    kb_path = "knowledge_base"

    if not os.path.exists(kb_path):
        return docs, filenames

    for file in os.listdir(kb_path):
        if file.endswith(".txt"):
            file_path = os.path.join(kb_path, file)

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    docs.append(text)
                    filenames.append(file)

    return docs, filenames

def query_kb(query, top_k=2):
    docs, filenames = load_docs()

    if not docs:
        return []

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(docs)
    q_vec = vectorizer.transform([query])

    scores = cosine_similarity(q_vec, X)[0]
    top_indices = scores.argsort()[-top_k:][::-1]

    results = []
    for i in top_indices:
        results.append({
            "content": docs[i],
            "source": filenames[i],
            "score": float(scores[i])
        })

    return results
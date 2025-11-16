# backend/search.py
import json
import os
from sentence_transformers import SentenceTransformer, util
import torch
from rapidfuzz import fuzz

# ===== Paths =====
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LAW_DB = os.path.join(DATA_DIR, "law_db.json")

# ===== Device =====
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[INFO] Using device for embeddings: {device}")

# ===== Model =====
model = SentenceTransformer("all-MiniLM-L6-v2", device=device)
embeddings = []

# ===== Load docs =====
def load_docs():
    if not os.path.exists(LAW_DB):
        return []
    with open(LAW_DB, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# ===== Refresh embedding index =====
def refresh_index():
    global embeddings
    embeddings.clear()
    docs = load_docs()
    contents = [d.get("noi_dung", "") for d in docs]
    if contents:
        embeddings.extend(model.encode(contents, convert_to_tensor=True))

# ===== Keyphrase search =====
def search_by_keyphrase(query):
    results = []
    for d in load_docs():
        for kp in d.get("keyphrase", []):
            if kp.lower() in query.lower():
                results.append(d)
                break
    return results

# ===== Fuzzy search =====
def fuzzy_search(query, docs):
    best = []
    for d in docs:
        score = fuzz.partial_ratio(query.lower(), d["noi_dung"].lower()) / 100
        if score > 0.6:
            d2 = dict(d)
            d2["score"] = score
            best.append(d2)
    return sorted(best, key=lambda x: x["score"], reverse=True)

# ===== Semantic search =====
def search_semantic(query, top_k=3):
    if not embeddings:
        return []

    query_emb = model.encode(query, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_emb, torch.stack(embeddings))[0]

    k = min(top_k, len(embeddings))
    top_results = torch.topk(cosine_scores, k=k)

    docs = load_docs()
    results = []

    for score, idx in zip(top_results.values, top_results.indices):
        doc = docs[idx]
        boost = 0.0
        for kp in doc.get("keyphrase", []):
            if kp.lower() in query.lower():
                boost += 0.08
        final_score = float(score) + boost
        doc_copy = dict(doc)
        doc_copy["score"] = round(final_score, 4)
        results.append(doc_copy)

    # Sort theo score
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results

# ===== Related questions =====
def get_related_questions(query, top_k=3):
    if not embeddings:
        return []
    query_emb = model.encode(query, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_emb, torch.stack(embeddings))[0]

    k = min(top_k + 1, len(embeddings))
    top_results = torch.topk(cosine_scores, k=k)

    docs = load_docs()
    related = []
    for idx in top_results.indices[1:]:  # bỏ top1
        related.append(docs[idx]["noi_dung"])
    return related

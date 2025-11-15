#file: backend/search.py
from tinydb import TinyDB
from sentence_transformers import SentenceTransformer, util
import torch
import os

DB_PATH = "data/law_db.json"
db = TinyDB(DB_PATH)

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = []

def init_embeddings():
    global embeddings
    embeddings.clear()
    contents = [item["noi_dung"] for item in db.all()]
    if contents:
        embeddings.extend(model.encode(contents, convert_to_tensor=True))

init_embeddings()

def search_by_keyphrase(query):
    results = []
    for item in db.all():
        for kp in item.get("keyphrase", []):
            if kp.lower() in query.lower():
                results.append(item)
                break
    return results

def search_semantic(query, top_k=1):
    if not embeddings:
        return None
    query_emb = model.encode(query, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_emb, torch.stack(embeddings))[0]
    k = min(top_k, len(embeddings))
    top_results = torch.topk(cosine_scores, k=k)
    all_items = db.all()
    results = []
    for score, idx in zip(top_results.values, top_results.indices):
        item = all_items[idx]
        item["score"] = float(score)
        results.append(item)
    return results[0] if results else None

def get_related_questions(query, top_k=3):
    if not embeddings:
        return []
    query_emb = model.encode(query, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_emb, torch.stack(embeddings))[0]

    k = min(top_k + 1, len(embeddings))  # đảm bảo không vượt quá DB
    top_results = torch.topk(cosine_scores, k=k)

    all_items = db.all()
    related = []
    for score, idx in zip(top_results.values[1:], top_results.indices[1:]):  # bỏ top 1
        related.append(all_items[idx]["noi_dung"])
    return related

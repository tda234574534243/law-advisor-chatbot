import os
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import sparse

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

LAW_DB = os.path.join(DATA_DIR, 'law_db.json')
VECT_PATH = os.path.join(MODELS_DIR, 'tfidf_vectorizer.pkl')
MATRIX_PATH = os.path.join(MODELS_DIR, 'tfidf_matrix.npz')
DOCIDS_PATH = os.path.join(MODELS_DIR, 'tfidf_doc_ids.json')


def load_docs():
    if not os.path.exists(LAW_DB):
        return []
    with open(LAW_DB, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_index(max_features=20000, ngram_range=(1,2)):
    docs = load_docs()
    texts = [d.get('noi_dung','') for d in docs]
    if not texts:
        print('[TFIDF] No documents found in law_db.json')
        return

    vectorizer = TfidfVectorizer(ngram_range=ngram_range, max_features=max_features)
    X = vectorizer.fit_transform(texts)

    # Save
    with open(VECT_PATH, 'wb') as f:
        pickle.dump(vectorizer, f)
    sparse.save_npz(MATRIX_PATH, X)
    doc_ids = [ { 'index': i, 'dieu': docs[i].get('dieu'), 'chuong': docs[i].get('chuong') } for i in range(len(docs)) ]
    with open(DOCIDS_PATH, 'w', encoding='utf-8') as f:
        json.dump(doc_ids, f, ensure_ascii=False, indent=2)

    print('[TFIDF] Built index:', X.shape)


if __name__ == '__main__':
    build_index()

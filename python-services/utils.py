from numpy import dot
from numpy.linalg import norm

def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))


def compute_score(model, query_embedding, doc):
    
    # doc_text = f"{doc['crop']} {doc['state']}"
    doc_text = f"information about {doc['crop']} crop in {doc['state']}"
    
    doc_embedding = model.encode(doc_text)

    score = cosine_similarity(query_embedding, doc_embedding)

    return score
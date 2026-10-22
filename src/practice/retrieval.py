# src/retrieval.py
STOPWORDS = {"is", "the", "of", "a", "in", "what", "where", "which"}

def tokenize(text):
    words = text.lower().replace(".", "").replace("?", "").replace("'s", "").split()
    return [w for w in words if w not in STOPWORDS]

def doc_frequency(word, corpus):
    return sum(1 for text in corpus.values() if word in tokenize(text))

def score(question, passage, corpus):
    q_words = set(tokenize(question))
    p_words = set(tokenize(passage))
    total = 0
    for word in q_words & p_words:
        total += 1 / doc_frequency(word, corpus)
    return total

def retrieve(question, corpus, k=1):
    scored = [(doc_id, score(question, text, corpus)) for doc_id, text in corpus.items()]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [(d, s) for d, s in scored[:k] if s > 0]

def recall_at_k(results, gold):
    if len(gold) == 0:
        return 0.0
    retrieved_ids = {doc_id for doc_id, _ in results}
    return len(retrieved_ids & gold) / len(gold)

def precision_at_k(results, gold, k):
    if k == 0:
        return 0.0
    retrieved_ids = {doc_id for doc_id, _ in results}
    return len(retrieved_ids & gold) / k

def mrr(results,gold):
    for rank, (doc_id,_) in enumerate(results,start=1):
        if doc_id in gold:
            return 1/rank
    return 0.0
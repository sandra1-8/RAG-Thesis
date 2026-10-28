corpus = {
    "d1": "Paris is the capital of France.",
    "d2": "Berlin is the capital of Germany.",
    "d3": "The Eiffel Tower is located in Paris.",
    "d4": "Mount Everest is the highest mountain on Earth.",
    "d5": "France is a country in Western Europe.",
    "d6": "Paris is the capital of France.",
    "d7": "Pariss is the captial of Frnace.",
    "d8": "Berlin is the capital of Germany and the largest city."
}

STOPWORDS = {"is", "the", "of", "a", "in", "what", "where"}

def tokenize(text):
    words = text.lower().replace(".","").replace("?","").split()
    return [w for w in words if w not in STOPWORDS]
def doc_frequency(word,corpus):
    """In how many documents does this word appear?"""
    return sum(1 for text in corpus.values() if word in tokenize(text))

for w in ["capital", "france", "paris", "mountain"]:
    print(w,doc_frequency(w,corpus))

def score(question,passage,corpus):
    # Count how many question words appear in the passage.
    q_words = set(tokenize(question))
    p_words = set(tokenize(passage))
    shared = q_words & p_words
    total = 0
    for word in shared:
        total += 1/doc_frequency(word,corpus)
    return total

def retreive(question,corpus,k=3):
    scored = [
        (doc_id,score(question,text,corpus))
        for doc_id, text in corpus.items()
    ]
    for doc_id, text in corpus.items():
        print(doc_id, score(question, text, corpus), text)

    scored.sort(key=lambda x:x[1], reverse=True)
    return scored[:k]

question = "What is the capital of France?"
# question = "Where is the Eiffel Tower?"
results = retreive(question,corpus,k=3)
# print(results)

# Evaluation: which docs are the gold evidence?
gold = {"d1"}

def recall_at_k(results,gold):
    retrieved_ids = {doc_id for doc_id,_ in results}
    return len(retrieved_ids & gold) / len(gold)

def precision_at_k(results, gold):
    retrieved_ids = {doc_id for doc_id,_ in results}
    return len(retrieved_ids & gold) / len(results)

def mrr(results,gold):
    for rank, (doc_id,_) in enumerate(results,start=1):
        if doc_id in gold:
            return 1/rank
    return 0.0
if __name__ == "__main__":
    print("Recall@3", recall_at_k(results,gold))
    print("Precision@3", precision_at_k(results,gold))
    print("mrr", mrr(results,gold))
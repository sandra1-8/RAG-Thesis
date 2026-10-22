# Lists
scores = [0.58,0.25,0.33,0.0]
print(len(scores))
print(scores[0])
print(max(scores))
print(sorted(scores,reverse=True))

# Dics
corpus = {"d1": "Paris is the capital of France.","d2": "Berlin is the capital of Germany."}
corpus["d3"] = "The Eiffel Tower is in Paris."
print(corpus["d1"])
for doc_id, text in corpus.items():
    print(doc_id,len(text))

# Function with a default value
def top_k(score_dict,k=2):
    ranked = sorted(score_dict.items(),key=lambda x:x[1],reverse=True)
    return ranked[:k]

my_scores = {"d1":0.58,"d2":0.25,"d5":0.33}
print(top_k(my_scores))
print(top_k(my_scores,k=1))

def mrr(results,gold):
    for rank, (doc_id,_) in enumerate(results,start=1):
        if doc_id in gold:
            return 1/rank
    return 0.0

# List comprehension : a loop in one line
lengths = [len(t) for t in corpus.values()]
long_docs = [d for d,t in corpus.items() if len(t)>30]
print(lengths,long_docs)
print(list(enumerate(["a", "b", "c"], start=1)))
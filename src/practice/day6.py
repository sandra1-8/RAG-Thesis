import math
import re
import json
import time
import copy
from collections import Counter
from pathlib import Path
from data_utils import build_corpus,build_gold
from retrieval import recall_at_k, precision_at_k, mrr

STOPWORDS = {"is","the","of","a","in","what","where","which","it"}

def tokenize(text):
    text = text.lower().replace("'s","")
    return [w for w in re.findall(r"[a-z0-9]+",text) if w not in STOPWORDS]

class TinyIndex:
    def __init__(self,corpus):
        self.corpus = corpus
        self.doc_tokens = {d: set(tokenize(t)) for d,t in corpus.items()}
        self.df = Counter()
        for tokens in self.doc_tokens.values():
            self.df.update(tokens)
        self.n = len(corpus)

    def idf(self,word):
        return math.log((self.n+1)/(self.df[word]+1))+1

    def search(self, question, k=3):
        q = set(tokenize(question))
        scores = {}
        for d, tokens in self.doc_tokens.items():
            s = sum(self.idf(w) for w in q & tokens)
            if s>0:
                scores[d] = s
        return sorted(scores.items(),key=lambda x:x[1], reverse = True)[:k]


ROOT = Path(__file__).resolve().parents[2] 

with open(ROOT/"data/toy_hotpot.json","r",encoding="utf-8") as f:
    loaded = json.load(f)
clean_corpus = build_corpus(loaded)
corpus = copy.deepcopy(clean_corpus)

meta = {} # the answer key for corruptions; the retriever never sees this

# Duplicates of Paris_0 and Berlin_0
corpus["Paris_0_dup1"] = "Paris is the capital of France."
meta["Paris_0_dup1"] = {"source":"Paris_0","type":"duplicate"}

corpus["Berlin_0_dup1"] = "Berlin is the capital of Germany."
meta["Berlin_0_dup1"] = {"source":"Berlin_0","type":"duplicate"}

# Typo versions
corpus["Paris_0_typo1"] = "Paris is the captial of France."
meta["Paris_0_typo1"] = {"source": "Paris_0", "type": "lexical", "severity": 1}

corpus["Berlin_0_typo1"] = "Berln is the capitla of Germany."
meta["Berlin_0_typo1"] = {"source": "Berlin_0", "type": "lexical", "severity": 2}

clean_index = TinyIndex(clean_corpus)
noisy_index = TinyIndex(corpus)

questions = ["Which country is Paris the capital of?","Which city is the capital of Germany?"]

# start = time.perf_counter()

# for _ in range(1000):
# for q in questions:
#     print("scores: ",index.search(q))

# end = time.perf_counter()

# index_time = end - start

# print("TinyIndex time:", index_time, "seconds")
assert set(meta) <= set(corpus)

def evaluate(index,q,gold,k):
    results = index.search(q,k=k)
    return (recall_at_k(results,gold),
            precision_at_k(results,gold,k=k),
            mrr(results,gold))

if __name__ == "__main__":
    for item in loaded:
        q = item["question"]
        gold = build_gold(item)
        print(q)
        for k in (1,2,3):
            print(f"  k={k} clean (R, P, MRR):", evaluate(clean_index, q, gold, k))
            print(f"  k={k} noisy (R, P, MRR):", evaluate(noisy_index, q, gold, k))
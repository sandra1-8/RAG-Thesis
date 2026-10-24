import json
import time
from retrieval import retrieve, recall_at_k, mrr, precision_at_k
from data_utils import build_gold, build_corpus
from pathlib import Path
data = [
    {
        "_id": "q1",
        "question": "Which country is Paris the capital of?",
        "answer": "France",
        "supporting_facts": [["Paris", 0]],
        "context": [
            ["Paris", ["Paris is the capital of France.", "It lies on the Seine."]],
            ["Berlin", ["Berlin is the capital of Germany."]],
            ["Everest", ["Mount Everest is the highest mountain on Earth."]],
        ],
    },
    {
        "_id": "q2",
        "question": "Which city is the capital of Germany?",
        "answer": "Berlin",
        "supporting_facts": [["Berlin", 0]],
        "context": [
            ["Berlin", ["Berlin is the capital of Germany.", "It is Germany's largest city."]],
            ["Paris", ["Paris is the capital of France."]],
            ["Everest", ["Mount Everest is the highest mountain on Earth."]],
        ],
    },
]

# # Write it to a file
ROOT = Path(__file__).resolve().parents[2] 
# with open(ROOT/"data/toy_hotpot.json","w",encoding="utf-8") as f:
#     json.dump(data,f,indent=2)

# Read it back
with open(ROOT/"data/toy_hotpot.json","r",encoding="utf-8") as f:
    loaded = json.load(f)

# item = loaded[0]
# print(item["question"])
# print(item["answer"])

K = 3
corpus = build_corpus(loaded)
for item in loaded:
    gold = build_gold(item)

    start = time.perf_counter()
    for _ in range(1000):
        results = retrieve(item["question"], corpus, k=K)
    end = time.perf_counter()
    index_time = end - start
    print("old retrieval time:", index_time, "seconds")

    print(item["question"])
    print(results)
    print("Gold:", gold)
    print("Recall:", recall_at_k(results, gold))
    print("Precision:", precision_at_k(results, gold,k=K))
    print("mrr: ", mrr(results,gold))

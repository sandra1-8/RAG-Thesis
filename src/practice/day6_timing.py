import time
from retrieval import retrieve
from day6 import TinyIndex,clean_corpus

q = "Which country is Paris the capital of?"
index = TinyIndex(clean_corpus)

start = time.perf_counter()
for _ in range(1000):
    index.search(q)
print("TinyIndex, 5 passages:", time.perf_counter() - start)

big_corpus = dict(clean_corpus)
for i in range(2000):
    big_corpus[f"x{i}"] = f"random filler words about topic {i}"

big_index = TinyIndex(big_corpus)

start = time.perf_counter()
for _ in range(1000):
    big_index.search(q)
print("TinyIndex, 2000 passages:", time.perf_counter() - start)

# Compare with the old scorer.
start = time.perf_counter()
for _ in range(1000):
    retrieve(q,big_corpus,k=3)
print("old retrieve, 2000 passages:", time.perf_counter() - start)

# Build the index time separately. TinyIndex(big_corpus) does its precomputation once. Time that on its own too:
start = time.perf_counter()
TinyIndex(big_corpus)
print("index build:", time.perf_counter() - start)
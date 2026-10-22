# Turn context into a passage corpus
def build_corpus(items):
    corpus = {}
    for item in items:
        for title, sentences in item["context"]:
            for j, sent in enumerate(sentences):
                corpus[f"{title}_{j}"] = sent
    return corpus

# Turn supporting_facts into gold passage IDs
def build_gold(item):
    return {f"{title}_{i}" for title, i in item["supporting_facts"]}
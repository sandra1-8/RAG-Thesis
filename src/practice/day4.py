import re
import random

STOPWORDS = {"is", "the", "of", "a", "in", "what", "where", "which"}

def tokenize_v1(text):
    words = text.lower().replace(".", "").replace("?", "").replace("'s", "").split()
    return [w for w in words if w not in STOPWORDS]

def tokenize_v2(text):
    words = re.findall(r"[a-z0-9]+",text.lower())
    return [w for w in words if w not in STOPWORDS]

# def char_swap(word):
#     word = list(word)
#     l = len(word)//2
#     c = word[l]
#     word[l] = word[l+1]
#     word[l+1] = c
#     return "".join(word)

def char_swap(word):
    if len(word) < 3:
        return word          # too short to swap safely
    word = list(word)
    i = len(word) // 2 - 1   # stay inside the word
    word[i], word[i+1] = word[i+1], word[i]
    return "".join(word)

def char_swap_random(word, rng):
    if len(word) < 3:
        return word
    i = rng.randint(0,len(word)-2)
    chars = list(word)
    chars[i], chars[i+1] = chars[i+1], chars[i]
    return "".join(chars)

rng = random.Random(7)
for w in ["capital","france","germany"]:
    print(char_swap_random(w,rng))


tests = [
    "Paris is the capital of France.",
    "It is Germany's largest city.",
    "Hello, world! (Test-case: 3.5 km)",
    "Pariss is the captial of Frnace.",
]
if __name__ == "__main__":
    for t in tests:
        print(t)
        print(" v1:", tokenize_v1(t))
        print(" v2:", tokenize_v2(t))
print(" swapped", char_swap("capital"))
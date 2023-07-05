import pickle

with open("pr.pickle", "rb") as f:
    p = f.read()

v = pickle.loads(p)
print(f"unpickled result: {v!r}")
assert v == 10+3

import dill

if __name__ == "__main__":
    with open("pr.pickle", "rb") as f:
        p = f.read()

    v = dill.loads(p)
    print(f"unpickled result: {v!r}")
    assert v == 10+3

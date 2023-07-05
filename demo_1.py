from picklerun import picklerun

@picklerun
def myfunction(x, foo=3):
    """hello this is myfunction docstring"""
    print("demo: inside payload myfunction")
    return x+foo

p = myfunction(10)

with open("pr.pickle", "wb") as f:
    f.write(p)

# check written value in the local process
import pickle
v = pickle.loads(p)
assert v == 10+3

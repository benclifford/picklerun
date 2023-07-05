import dill

# TODO: would be interesting as a decorator to capture function invocation
# syntax on the serialization side?

# try first with dill, as i think thats easier

def runsource(body, name, args):
    exec(body)
    # return locals()[name](args)
    return locals()["payload"](*args)

class PickleRun:
    def __init__(self, src, name, args, kwargs):
        self.src = src
        self.name = name
        self.args = args
        self.kwargs = kwargs


    def __reduce__(self):
        print(f"picklerun reducer: got source: {self.src}")

        return (runsource, (self.src, self.name, self.args))


def picklerun(f):
    """A decorator to run a function call at deserialization time.

    This invariant should roughly hold:

    dill.loads(picklerun(f)(1)) == f(1)
    """
    # this includes the decorator...
    src = dill.source.getsource(f, lstrip=True, alias="payload")

    # so what's a nice way to remove it?
    # could look for the first line being @picklerun, which is
    # pretty horrible...
    print(f"picklerun decorator: got source: {src}")

    lines = src.split("\n")
    lines = [l for l in lines if l != "@picklerun"]
    src = "\n".join(lines)

    print(f"picklerun decorator: filtered src: {src}")

    def wrapped(*args, **kwargs):
        return dill.dumps(PickleRun(src, f.__name__, args=args, kwargs=kwargs))

    return wrapped

if __name__ != "__main__":
    raise RuntimeError("this module isn't allowed to be imported")
else:
    @picklerun
    def myfunction(x, foo=3):
        """hello this is myfunction docstring"""
        print("demo: inside payload myfunction")
        return x+foo

    p = myfunction(10)
    print(f"demo: top level pickle stream: {p!r}")

    with open("pr.pickle", "wb") as f:
        f.write(p)

    v = dill.loads(p)
    print(f"demo: unpickled result: {v!r}")
    assert v == 10+3

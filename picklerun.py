import dill

# TODO: would be interesting as a decorator to capture function invocation
# syntax on the serialization side?

# try first with dill, as i think thats easier

class PickleRun:
    def __init__(self, f, args, kwargs):
        self.f = f
        self.args = args
        self.kwargs = kwargs

    def __reduce__(self):
        return (self.f, self.args)

def picklerun_f(f, args=[], kwargs={}):
    """Invoke f(*args, **kwargs) at deserialization.
    The result of the function call will be returned as the deserialized
    object.
    """

    return dill.dumps(PickleRun(f, args, kwargs))


def picklerun(f):
    """A decorator to run a function call at deserialization time.

    This invariant should roughly hold:

    dill.loads(picklerun(f)(1)) == f(1)
    """

    def wrapped(*args, **kwargs):
        return picklerun_f(f, args=args, kwargs=kwargs)

    return wrapped

if __name__ != "__main__":
    raise RuntimeError("this module isn't allowed to be imported")
else:
    @picklerun
    def myfunction(x, foo=3):
        """hello this is myfunction docstring"""
        print("running myfunction")
        return x+foo

    p = myfunction(10)
    # p = picklerun_f(myfunction, (10, ))
    print(f"pickle stream: {p!r}")

    with open("pr.pickle", "wb") as f:
        f.write(p)

    v = dill.loads(p)
    print(f"unpickled result: {v!r}")
    assert v == 10+3

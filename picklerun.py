import dill
import pickle

class PickleRun:
    def __init__(self, src, args, kwargs):
        self.src = src
        self.args = args
        self.kwargs = kwargs


    def __reduce__(self):
        print(f"picklerun reducer: got source: {self.src}")

        return (eval, ("(exec(b), payload(*a))[-1]", None, {"b": self.src, "a": self.args}))


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
        return pickle.dumps(PickleRun(src, args=args, kwargs=kwargs))

    return wrapped

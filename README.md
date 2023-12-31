picklerun
=========

Run function invocations remotely inside pickle deserialization


    "It is possible to construct malicious pickle
     data which will execute arbitrary code during
     unpickling"
         -- https://docs.python.org/3/library/pickle.html

... but they don't give you much help doing so...  picklerun aims to solve this usability problem.


Usage:

```
from picklerun import picklerun

@picklerun
def myfunc(x):
    print("I am executing inside the deserialiser!")
    return x+1

bytestream = myfunc(3)

import pickle


# outputs: "I am executing inside the deserialiser!" at this line
assert pickle.loads(bytestream) == 3+1
```

REQUIREMENTS
============

You'll need `pip install dill` on the creation side, but not on the
deserialisation side.

BUGS
====

kwargs aren't implemented. I don't think would be hard, though.

This gets source using dill.source. That has this problems:

* it is awkward to remove the decorator from the source code. Right now
  a literal `@picklerun` is removed if present, but using any other
  naming won't work - such as `@picklerun.picklerun` or:
  ```
  from picklerun import picklerun as p
  
  @p
  def myfunc():
      ...
  ```

RELATED
=======

[Never a dill moment: Exploiting machine learning pickle files](https://blog.trailofbits.com/2021/03/15/never-a-dill-moment-exploiting-machine-learning-pickle-files/)

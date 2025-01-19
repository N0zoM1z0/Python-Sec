import pickle
import pickletools

class Secret(object):
    def __init__(self, name):
        self.name = name

s = Secret('pwn')
opcode = b"""c__main__
s
(S'name'
S'own'
db."""

pickle.loads(opcode)
print(s.name)
pickletools.dis(opcode)
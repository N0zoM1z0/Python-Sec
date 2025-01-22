from flask import *
from jinja2 import Template

app = Flask(__name__)


@app.route('/template_file', methods=['GET', 'POST'])
def template_file():
    title = "Flask Render Template Example"
    message = "Welcome to Flask with render_template!"

    username = None
    if request.method == 'POST':
        username = request.form.get('username')

    return render_template('index.html', title=title, message=message, username=username)


@app.route('/template_string', methods=['GET', 'POST'])
def template_string():
    title = "Flask Render Template String Example"
    message = "Welcome to Flask with render_template_string!"

    username = None
    if request.method == 'POST':
        username = request.form.get('username')

    # 使用 render_template_string 来渲染模板字符串
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>
    </head>
    <body>
        <h1>{{ message }}</h1>
        <form method="post">
            <label for="username">Enter your username:</label>
            <input type="text" id="username" name="username" value="{{ username }}" required>
            <button type="submit">Submit</button>
        </form>
        {% if username %}
            <p>Welcome, {{ username }}!</p>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(template, title=title, message=message, username=username)
    # This is safe!!! No SSTI

@app.route("/ssti1", methods = ['GET'])
def ssti1():
    name = request.args.get('name', 'guest')
    ts = Template("Hello " + name)
    return ts.render()

@app.route("/safe_ssti", methods = ['GET'])
def safe_ssti():
    name = request.args.get('name', 'guest')
    ts = Template("Hello {{n}}")
    return ts.render(n=name)

app.secret_key = 'your_secret_key'  # 必须设置，用于加密 session 数据

@app.route('/set_session', methods=['GET'])
def set_session():
    """
    设置会话变量
    URL 示例: /set_session?key=username&value=JohnDoe
    """
    key = request.args.get('key')  # 从请求参数获取 'key'
    value = request.args.get('value')  # 从请求参数获取 'value'

    if key and value:
        session[key] = value  # 使用 Flask 内置的 session 设置会话变量
        return jsonify({"message": f"Session variable '{key}' set to '{value}'!"}), 200
    else:
        return jsonify({"error": "Missing 'key' or 'value' parameter!"}), 400


@app.route('/get_session', methods=['GET'])
def get_session():
    """
    获取会话变量
    URL 示例: /get_session?key=username
    """
    key = request.args.get('key')  # 从请求参数获取 'key'

    if key:
        value = session.get(key)  # 获取会话变量
        if value:
            return jsonify({"key": key, "value": value}), 200
        else:
            return jsonify({"error": f"Session variable '{key}' not found!"}), 404
    else:
        return jsonify({"error": "Missing 'key' parameter!"}), 400


@app.route('/clear_session', methods=['GET'])
def clear_session():
    """
    清空所有会话数据
    """
    session.clear()  # 清空会话
    return jsonify({"message": "All session variables cleared!"}), 200

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug = True)
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/json_example', methods=['POST'])
def add_user():
    content = request.json
    return jsonify(content)


if __name__ == '__main__':
    app.run()
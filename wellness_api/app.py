from flask import Flask, jsonify, request

app = Flask(__name__)
test = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    },
]
@app.route('/test', methods=['GET'])
def get_test():
    return jsonify(test)

def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
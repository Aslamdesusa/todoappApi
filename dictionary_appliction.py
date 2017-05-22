from flask import Flask, abort, jsonify, make_response, request

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)
app.config.update({
    "DEBUG": True
})

users = [
    {'name':'aslam','password':'python'}
    ]

words = [
    {
        'id': 1,
        'username': 'aslam',
        'word': 'botal',
        'note': 'nothing ',
        'difficulty': '8',
    },
    {
        'id': 7,
        'username': 'aslam',
        'word': 'botal',
        'note': 'botal jisme ',
        'difficulty': '2',
    },
    {
        'id': 6,
        'username': 'aslam',
        'word': 'akhand chutiyappa',
        'note': 'bekaar ',
        'difficulty': '7',
    },
    {
        'id': 3,
        'username': 'aslam',
        'word': 'akhand chutiyappa',
        'note': 'bekaar ',
        'difficulty': '7',
    },
    {
        'id': 2,
        'username': 'aslam',
        'word': 'akhand chutiyappa',
        'note': 'bekaar ',
        'difficulty': '7',
    }

]

@auth.get_password
def get_password(username):
    new = [user for user in users if username == user['name']]
    if len(new)==0:
        abort (404)
    return new[0]['password']

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'errror': 'unauthorized'}),401)

@app.route('/user/get_word',methods=['GET'])
@auth.login_required
def get_words():
    word = [word for word in words if auth.username() == word['username']]
    input = request.args.get('input')
    if input == 'id':
        word = sorted(word, key=lambda t: t['id'])
    elif input == 'difficulty':
        word = sorted(word, key=lambda t: t['difficulty'])
    elif input == 'word':
        word = sorted(word, key=lambda t: t['word'])
    return jsonify({'word': word})

@app.route('/add/sign', methods = ['POST'])
def adding():
    if not request.json or not 'name' in request.json:
        abort(400)
    add = {
        'name': request.json['name'],
        'password': request.json['password']
    }
    users.append(add)
    return jsonify({'userss': add}), 201

@app.route('/add/post', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'word' in request.json:
        abort(400)
    new_words = {
        'id': words[-1]['id'] + 1,
        'username': auth.username(),
        'word': request.json['word'],
        'note': request.json['note'],
        'difficulty': request.json['difficulty']
    }
    words.append(new_words)
    return jsonify({'task': new_words}), 201



if __name__ == "__main__":
    app.run()
from functools import wraps

import jwt
from sanic import Sanic
from sanic.response import json

app = Sanic()

SECRET = 'thesecret'

empty_token = {'authenticated', False}


class Token:

    def __init__(self, token=None, data=None, algorithm='HS256'):
        # will take token over data
        if token:
            data = self.load_token(token)
        self.data = data if data else {}
        self.algorithm = algorithm

    def load_token(self, token):
        return jwt.decode(token, SECRET)

    @property
    def token(self):
        return jwt.encode(self.data, SECRET, algorithm=self.algorithm)

    @property
    def header(self):
        return {'Authorization': 'Bearer: {}'.format(str(self.token, 'ASCII'))}


@app.middleware('request')
async def load_jwt(request):
    request.args['Token'] = Token(token=request.token)

@app.middleware('response')
async def dump_jwt(request, response):
    response.headers.update(request.args['Token'].header)

@app.route('/')
async def test(request):
    return json({'message': 'Hello World'})

@app.route('/counter/')
async def counter(request):
    count = request.args['Token'].data.get('count', 0)
    request.args['Token'].data['count'] = count + 1
    return json({'message': "You've clicked {} times".format(count)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

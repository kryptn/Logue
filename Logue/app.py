import jwt
from sanic import Sanic
from sanic.response import json

app = Sanic()

secret = 'thesecret'

def get_jwt(payload):
    return jwt.encode(payload, secret, algorithm='HS256')

def read_jwt(token):
    return jwt.decode(token, secret)

def build_jwt(payload):
    return {'Authorization': 'Bearer {}'.format(get_jwt(payload))}

@app.route('/')
async def test(request):
    return json({'message': 'Hello World'},
            headers=build_jwt({'authed': False}),
            status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

from flask import Flask, request;

app = Flask(__name__)

@app.get('/users')
def get_all_users():
    '''Gets a list of all users'''


@app.get('/user/:id')
def get_user():
    '''Get data on one user'''



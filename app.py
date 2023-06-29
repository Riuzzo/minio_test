from flask import Flask, jsonify
import requests
import os
from storage_minIO import Storage

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/files')
def files():
    storage = Storage('localhost:9000', 'minioadmin', 'minioadmin')
    storage.make_bucket('test')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
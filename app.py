from flask import Flask, jsonify
import io
import time
import requests
import os
import json
from storage_minIO import Storage

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/files')
def files():
    storage = Storage('storage:9000', 'minioadmin', 'minioadmin')

    start = time.time()
    storage.bucket_exist('test7')
    bucketExistTime = time.time() - start

    if not storage.bucket_exist('test10') :
        storage.make_bucket('test10')

    start = time.time()
    storage.file_exist('test7', 'prova/test.json')
    fileExistTime = time.time() - start

    if not storage.file_exist('test7', 'prova/test.json'): 
        file1 = '{"name": "test_file", "time": "now"}'

        data = json.dumps(file1).encode("utf-8")
        data_stream = io.BytesIO(data)
        data_stream.seek(0)

        start = time.time()
        storage.put_file('test7', 'prova/test.json', data_stream, len(data))
        putFileTime = time.time() - start
    else:
        storage.delete('test9', 'prova/test1.json')

    start = time.time()
    dataFile = storage.get_file('test4', 'prova/test.json')
    dataFileTime = time.time() - start

    start = time.time()
    dataLink = storage.get_link('test4', 'prova/test.json')
    dataLinkTime = time.time() - start

    start = time.time()
    dataList = storage.list('test7', recursive=True)
    dataListTime = time.time() - start

    string = ''
    for data in dataList:
        string = string + str(data.object_name)

    start = time.time()
    storage.copy('test9', 'prova/test2.json', 'test7', 'prova/test2.json')
    copyTime = time.time() - start
    
    return str(copyTime) + ', ' + str(bucketExistTime) + ', ' + str(fileExistTime) + ', ' + str(dataFileTime) + ', ' + str(dataLinkTime) + ', ' + str(dataListTime)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
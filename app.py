from flask import Flask, jsonify
import io
import time
import json
from storage_minIO import Storage
from storage_owncloud import Storage_owncloud

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/files')
def files():
    storage = Storage_owncloud('https://b2drop.eudat.eu')
    start = time.time()
    storage.connect('ab1fdb5b-83a4-42b8-8d0a-c9fe599a82df', '4rxCq-Ntayt-qz7dB-WDSAM-Kc4p9')
    loginTime = time.time() - start

    start = time.time()
    storage.bucket_exist('test1')
    bucketExistTime = time.time() - start

    if not storage.bucket_exist('test1') :
        start = time.time()
        storage.make_bucket('test1')
        makeBucketTime = time.time() - start

    start = time.time()
    storage.file_exist('test1', 'embeddings.json')
    fileExistTime = time.time() - start

    if not storage.file_exist('test1', 'embeddings.json'): 
        #data = json.dumps(file1).encode("utf-8")
        #data_stream = io.BytesIO(data)
        #data_stream.seek(0)

        start = time.time()
        storage.put_file_from_path('test1', 'embeddings.json', 'embeddings.json')
        putFileTime = time.time() - start

        start = time.time()
        storage.delete('test1', 'embeddings.json')
        deleteFileTime = time.time() - start

        storage.delete_bucket('test1')
    else:
        storage.delete('test9', 'prova/test1.json')

    ##storage.make_bucket('test5')
    ##storage.put_file_from_path('test5', 'embeddings.json', 'embeddings.json')
    ##storage.put_file_from_path('test5', 'embeddings2.json', 'embeddings.json')
    ##storage.put_file_from_path('test5', 'embeddings.json', 'embeddings.json')
    ##storage.put_file_from_path('test5', 'prova/embeddings.json', 'embeddings.json')
    ##storage.put_file_from_path('test5', 'prova/test/embeddings1.json', 'embeddings.json')
    ##storage.put_file_from_path('test5', 'prova/test/embeddings.json', 'embeddings.json')
    ##storage.put_file_from_path('test5', 'prova/test/embeddings2.json', 'embeddings.json')

    start = time.time()
    dataFile = storage.get_file('test5', 'embeddings.json')
    dataFileTime = time.time() - start

    start = time.time()
    dataLink = storage.get_link('test5', 'embeddings.json')
    dataLinkTime = time.time() - start

    start = time.time()
    dataList = storage.list('test5', recursive=True)
    dataListTime = time.time() - start

    string = ''
    for data in dataList:
        string = string + str(data.object_name)

    ##storage.make_bucket('test2')
    start = time.time()
    storage.copy('test2', 'embeddings.json', 'test5', 'embeddings.json')
    copyTime = time.time() - start
    storage.delete('test2', 'embeddings.json')

    ##storage.make_bucket('test')
    start = time.time()
    ##storage.snowball_upload('test', [{'path': '0.png', 'name': '0.png'}, {'path': 'embeddings.json', 'name': 'embeddings.json'}, {'path': 'labels.json', 'name': 'labels.json'}, {'path': 'metadata.json', 'name': 'metadata.json'}, {'path': 'reduction.json', 'name': 'reduction.json'}, {'path': '000001.png', 'name': '000001.png'}])
    snowballTime = time.time() - start
    
    return  str(loginTime) + '\n' + str(bucketExistTime) + '\n' + str(makeBucketTime) + '\n' + str(fileExistTime) + '\n' + str(putFileTime) + '\n' + str(deleteFileTime) + '\n' + str(dataFileTime) + '\n' + str(dataLinkTime) + '\n' + str(dataListTime) + '\n' + str(copyTime)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
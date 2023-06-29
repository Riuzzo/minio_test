import minio
from minio import Minio
from minio.error import ResponseError
#from minio.copyconditions import CopySource
from requests.exceptions import ConnectionError

from retry import retry

class Storage():
    def __init__(self, host, access_key, secret_key):
        self.client = Minio(host, access_key=access_key, secret_key=secret_key, secure=False)

    @retry(exceptions=(ConnectionError))
    def bucket_exist(self, bucket_name):
        try:
            return self.client.bucket_exists(bucket_name)

        except ResponseError as exception:
            print('storage exception:\n\t{}\n\t{}'.format(exception, bucket_name))
            return False
        
    @retry(exceptions=(ConnectionError))
    def file_exist(self, bucket_name, file_path):
        try:
            return self.client.stat_object(bucket_name, file_path)

        except ResponseError as exception:
            print('storage exception:\n\t{}\n\t{}'.format(exception, file_path))
            return False
        
    @retry(exceptions=(ConnectionError))
    def list(self, bucket_name, prefix=None, recursive=False):
        return self.client.list_objects(bucket_name, prefix=prefix, recursive=recursive)
    
    @retry(exceptions=(ConnectionError))
    def get_file(self, bucket_name, file_path):
        return self.client.get_object(bucket_name, file_path)
    
    @retry(exceptions=(ConnectionError))
    def get_link(self, bucket_name, file_path):
        return self.client.presigned_get_object(bucket_name, file_path)
    
    # A quanto pare minio non permette la creazione di folder vuoti, 
    # ma va a creare le directory nel momento in cui si inserisce un file in un bucket; 
    # per esempio, andando ad inserire il file photos/photo1.jpg,
    # minio creerà la directory photos e al suo interno il file photo1.jpg
    
    #@retry(exceptions=(ConnectionError))
    #def mkdir(self, bucket_name, dir_path):

    
    @retry(exceptions=(ConnectionError))
    def make_bucket(self, bucket_name):
        return self.client.make_bucket(bucket_name)
    
    @retry(exceptions=(ConnectionError))
    def copy(self, bucket_name, file_name, new_bucket_name, new_file_name):
        return self.client.copy_object(bucket_name, file_name, CopySource(new_bucket_name, new_file_name))
    
    @retry(exceptions=(ConnectionError))
    def put_file(self, bucket_name, file_name, file_data):
        return self.client.put_object(bucket_name, file_name, file_data)
    
    @retry(exceptions=(ConnectionError))
    def delete(self, bucket_name, file_name):
        return self.client.remove_object(bucket_name, file_name)
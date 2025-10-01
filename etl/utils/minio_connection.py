from minio import Minio
from minio.error import S3Error
import io


class MinioClient:
    def __init__(self, endpoint, access_key, secret_key, secure=False):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )

    def create_bucket(self, bucket_name):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

    def upload_file(self, bucket_name, object_name, file_path):
        try:
            self.client.fput_object(bucket_name, object_name, file_path)
            return True
        except S3Error as e:
            raise Exception(f"Error al subir archivo a MinIO: {e}")

    def download_file(self, bucket_name, object_name, file_path):
        try:
            self.client.fget_object(bucket_name, object_name, file_path)
            return True
        except S3Error as e:
            raise Exception(f"Error al descargar archivo de MinIO: {e}")

    def upload_bytes(self, bucket_name, object_name, data: bytes):
        data_stream = io.BytesIO(data)
        self.client.put_object(bucket_name, object_name, data_stream, len(data))

    def get_object(self, bucket_name, object_name):
        try:
            response = self.client.get_object(bucket_name, object_name)
            return response.read()
        finally:
            response.close()
            response.release_conn()

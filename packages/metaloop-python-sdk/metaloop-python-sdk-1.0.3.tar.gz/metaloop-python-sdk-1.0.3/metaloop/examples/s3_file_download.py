import time

from metaloop.client import MDS, CloudConfig, CloudClient


def get_cloud_storage_config(
        x_api,
        name: str,
        storage_type: str = ""
) -> CloudConfig:
    if not CloudClient.find_s3_config(name):
        info = x_api.get_authorized_s3_config(name, storage_type)
        identifier = info["name"]
        endpoint = info["endpoint"]
        access_key = info["access_key"]
        secret_key = info["secret_key"]
        default_bucket = info["bucket"]

        CloudClient.set_s3_config(identifier, endpoint, access_key, secret_key, default_bucket)
    else:
        identifier = name

    return CloudClient.find_s3_config(identifier)


if __name__ == '__main__':
    mds_client = MDS("4057deac-6700-47d8-a4fc-a3c4854502a0", "http://192.168.100.71:30301")
    file_list = ['/metaloop227/0d214d2e-c63e-4005-a32a-ca1a6183d4ec/sample_test/234.jpg']
    index = 0
    for url in file_list:
        if url.startswith('/'):
            items = url.strip("/").split("/")
            bucket = items[0]
            key = '/'.join(items[1:])
            s3_config = get_cloud_storage_config(mds_client.x_api, bucket)
            with open(str(index)+'.jpg', 'wb') as data:
                CloudClient.download_fileobj(s3_config.identifier, bucket, key, data)
        else:
            s3_config = get_cloud_storage_config(mds_client.x_api, 'local')
            with open(str(index) + '.jpg', 'wb') as data:
                CloudClient.download_fileobj(s3_config.identifier, s3_config.default_bucket, url, data)
        index += 1

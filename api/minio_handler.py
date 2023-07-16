from minio import Minio
from minio.error import S3Error


def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        endpoint="s3.greedandfear.fun",
        access_key="miniopython",
        secret_key="O9FNbVbZVD47cEgiAb8nH8548l0ZqYh2b7q61m9L"
    )

    # Make 'asiatrip' bucket if not exist.
    # obj = client.get_presigned_url(bucket_name="stock",object_name="logo.jpg",method="GET")

    stocks = client.list_objects(bucket_name="stock")

    # print(obj)
    
    # client.remove_bucket('asiatrip')
    # if not found:
    #     client.make_bucket("asiatrip")
    # else:
    #     print("Bucket 'asiatrip' already exists")

    # Upload '/home/user/Photos/asiaphotos.zip' as object name
    # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
    # client.fput_object(
    #     "asiatrip", "asiaphotos-2015.zip", "/home/user/Photos/asiaphotos.zip",
    # )
    # print(
    #     "'/home/user/Photos/asiaphotos.zip' is successfully uploaded as "
    #     "object 'asiaphotos-2015.zip' to bucket 'asiatrip'."
    # )


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)
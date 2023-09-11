from minio import Minio
from minio.error import S3Error


def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        
        endpoint="139.59.22.99:9000",
        access_key="miniopython",
        secret_key="O9FNbVbZVD47cEgiAb8nH8548l0ZqYh2b7q61m9L"
        ,secure=False
    )

    # Make 'asiatrip' bucket if not exist.
    # obj = client.get_presigned_url(bucket_name="logo",object_name="logo.jpg",method="GET")

    bucket_name = "logopics"

    stocks = client.list_objects(bucket_name=f"{bucket_name}")

    for each_stock in stocks:
        print(each_stock.object_name)
        client.fget_object(bucket_name=f"{bucket_name}",file_path=f"{bucket_name}/{each_stock.object_name}",object_name=each_stock.object_name)

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
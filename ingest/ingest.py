import os
import time
import boto3
import pandas as pd
import kagglehub
from botocore.exceptions import ClientError

# -------------------------------------------------------
# CONFIG
# -------------------------------------------------------
S3_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "http://minio:9000")
S3_BUCKET = os.environ.get("MINIO_BUCKET", "data-bucket")
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# -------------------------------------------------------
# 1. AGUARDAR O MINIO SUBIR
# -------------------------------------------------------
print("Aguardando MinIO iniciar...")

while True:
    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name="us-east-1",
        )
        s3.list_buckets()
        print("MinIO respondeu. Continuando...")
        break
    except Exception as e:
        print("MinIO ainda não está pronto. Tentando novamente em 2s...")
        time.sleep(2)

# -------------------------------------------------------
# 2. DOWNLOAD DO DATASET
# -------------------------------------------------------
print("Baixando dataset do Kaggle...")

path_to_download_dir = kagglehub.dataset_download("marshalpatel3558/diabetes-prediction-dataset-legit-dataset")

csv_filename = "Dataset of Diabetes .csv"
full_csv_path = os.path.join(path_to_download_dir, csv_filename)

if not os.path.exists(full_csv_path):
    raise FileNotFoundError(full_csv_path)

df = pd.read_csv(full_csv_path)
print("Dataset carregado:", df.shape)

# -------------------------------------------------------
# 3. CRIAR BUCKET SE NÃO EXISTIR
# -------------------------------------------------------
print("Verificando bucket...")

try:
    s3.head_bucket(Bucket=S3_BUCKET)
    print("Bucket já existe.")
except ClientError:
    print("Bucket não existe. Criando...")
    s3.create_bucket(Bucket=S3_BUCKET)
    print("Bucket criado com sucesso.")

# -------------------------------------------------------
# 4. UPLOAD DO CSV
# -------------------------------------------------------
object_key = "raw/diabetes_dataset.csv"
tmp_local = "/tmp/diabetes_dataset.csv"

df.to_csv(tmp_local, index=False)

print("Enviando arquivo...")
s3.upload_file(tmp_local, S3_BUCKET, object_key)

print("Upload concluído!")
print("Arquivo disponível em:")
print(f"s3://{S3_BUCKET}/{object_key}")
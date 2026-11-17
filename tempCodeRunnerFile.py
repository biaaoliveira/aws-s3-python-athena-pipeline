import boto3
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

BUCKET = "datalake-raw-bianca-oliveira-2026"
ARQUIVO = "vendas/vendas.csv"

s3 = boto3.client("s3")


response = s3.get_object(Bucket=BUCKET, Key=ARQUIVO
)

df = pd.read_csv(BytesIO(response['Body'].read())) 

print("Quantidade inicial:", len(df))

# 1. Verificar valores nulos
print("\nValores nulos:")
print(df.isnull().sum())
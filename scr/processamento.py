import boto3
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

BUCKET_RAW = "datalake-raw-bianca-oliveira-2026"
BUCKET_PROCESSED = "datalake-processed-bianca-oliveira-2026"

ARQUIVO = "vendas/vendas.csv"

s3 = boto3.client("s3")

response = s3.get_object(Bucket=BUCKET_RAW, Key=ARQUIVO
)

df = pd.read_csv(BytesIO(response['Body'].read())) 

print("Quantidade inicial:", len(df))

print("\nValores nulos:")
print(df.isnull().sum())

df = df.drop_duplicates()

df = df.dropna(subset=[
    "id_venda",
    "data",
    "produto",
    "quantidade",
    "valor_unitario"
])

df = df[
    (df["quantidade"] > 0) &
    (df["valor_unitario"] > 0)
].copy()

df["data"] = pd.to_datetime(df["data"])

df["valor_total"] = (
    df["quantidade"] * df["valor_unitario"]
)

df["ano"] = df["data"].dt.year
df["mes"] = df["data"].dt.month

print(df[["data", "ano", "mes"]].head())

print("\n--- DADOS TRATADOS ---")
print(df.head())

print("\nTotal de registros após tratamento:", len(df))

print("\nFaturamento total:")
print(df["valor_total"].sum())

buffer = BytesIO()

df.to_parquet(
 buffer,
 index=False,
 engine="pyarrow",
 compression="snappy"
)

buffer.seek(0)


print("Conversão para Parquet concluída!")
print("Tamanho do arquivo:", buffer.getbuffer().nbytes, "bytes")

DESTINO = "vendas/vendas.parquet"

s3.put_object(
    Bucket=BUCKET_PROCESSED,
    Key=DESTINO,
    Body=buffer.getvalue()
)

print("Arquivo Parquet enviado para o S3!")

for (ano, mes), grupo in df.groupby(["ano", "mes"]):

    buffer_particao = BytesIO()

    grupo.drop(columns=["ano", "mes"]).to_parquet(
        buffer_particao,
        index=False,
        engine="pyarrow",
        compression="snappy"
    )

    destino_particao = (
        f"vendas_particionadas/"
        f"ano={ano}/"
        f"mes={mes:02d}/"
        f"dados.parquet"
    )

    s3.put_object(
        Bucket=BUCKET_PROCESSED,
        Key=destino_particao,
        Body=buffer_particao.getvalue()
    )

    print(f"Partição enviada: {destino_particao}")
import boto3
import pandas as pd
from io import BytesIO

s3 = boto3.client("s3")

BUCKET_RAW = "datalake-raw-bianca-oliveira-2026"
BUCKET_PROCESSED = "datalake-processed-bianca-oliveira-2026"

def lambda_handler(event, context):

    resposta = s3.get_object(
        Bucket=BUCKET_RAW,
        Key="vendas/vendas.csv"
    )

    df = pd.read_csv(BytesIO(resposta["Body"].read()))

    print("Registros recebidos:", len(df))

    # 2. Limpar os dados
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

    buffer = BytesIO()

    df.to_parquet(
        buffer,
        index=False,
        engine="pyarrow",
        compression="snappy"
    )

    destino = "vendas/vendas.parquet"

    s3.put_object(
        Bucket=BUCKET_PROCESSED,
        Key=destino,
        Body=buffer.getvalue()
    )

    print("Arquivo Parquet enviado com sucesso!")
    print("Registros processados:", len(df))

    return {
        "statusCode": 200,
        "body": "Pipeline executado com sucesso!"
    }

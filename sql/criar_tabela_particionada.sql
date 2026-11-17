CREATE EXTERNAL TABLE IF NOT EXISTS db_vendas.tb_vendas_particionadas (
    id_venda BIGINT,
    data TIMESTAMP,
    produto STRING,
    categoria STRING,
    regiao STRING,
    quantidade BIGINT,
    valor_unitario DOUBLE,
    valor_total DOUBLE
)
PARTITIONED BY (
    ano INT,
    mes STRING
)
STORED AS PARQUET
LOCATION 's3://datalake-processed-bianca-oliveira-2026/vendas_particionadas/';

MSCK REPAIR TABLE db_vendas.tb_vendas_particionadas;

SHOW PARTITIONS db_vendas.tb_vendas_particionadas;

# Arquitetura do Pipeline de Dados — AWS

## 1. Visão geral

Este projeto implementa um pipeline de Engenharia de Dados utilizando serviços da Amazon Web Services (AWS).

O objetivo é automatizar a ingestão, o processamento, o armazenamento e a consulta de dados de vendas, utilizando uma arquitetura baseada em Data Lake.

O pipeline recebe arquivos CSV no Amazon S3, executa transformações com Python e AWS Lambda, armazena os dados processados em formato Parquet e disponibiliza consultas SQL por meio do Amazon Athena.

## 2. Fluxo da arquitetura

```text
            ARQUIVO CSV
                 |
                 v
        +-----------------+
        |  Amazon S3 RAW  |
        |    vendas.csv   |
        +-----------------+
                 |
                 | Evento ObjectCreated
                 v
        +-----------------+
        |   AWS Lambda    |
        | Python + Pandas |
        +-----------------+
                 |
                 | Limpeza e transformação
                 v
        +-----------------+
        | S3 PROCESSED    |
        | vendas.parquet  |
        +-----------------+
                 |
                 v
        +-----------------+
        | AWS Glue Data   |
        |     Catalog     |
        +-----------------+
                 |
                 v
        +-----------------+
        |  Amazon Athena  |
        |   Consultas SQL |
        +-----------------+
```

O AWS Glue Data Catalog registra os metadados dos arquivos armazenados no S3. O Athena utiliza esses metadados para consultar os dados diretamente no Data Lake.

## 3. Serviços utilizados

### Amazon S3

Responsável pelo armazenamento dos dados em duas camadas:

**RAW — Dados brutos**

Bucket: `datalake-raw-bianca-oliveira-2026`

Armazena os arquivos CSV originais, preservando os dados recebidos antes das transformações.

**PROCESSED — Dados tratados**

Bucket: `datalake-processed-bianca-oliveira-2026`

Armazena os arquivos transformados em formato Parquet, utilizando compressão Snappy.

### AWS Lambda

Responsável por executar o processamento dos dados sem a necessidade de manter servidores.

A função `processamento-vendas` é acionada por eventos de criação de objetos no bucket RAW.

O processamento realiza:

1. Leitura do arquivo CSV utilizando Boto3.
2. Remoção de registros duplicados.
3. Remoção de registros com valores nulos em campos obrigatórios.
4. Exclusão de registros com quantidades ou preços inválidos.
5. Conversão da coluna de data.
6. Criação da coluna `valor_total`, calculada multiplicando quantidade por valor unitário.
7. Conversão dos dados para Parquet.
8. Armazenamento do resultado no bucket PROCESSED.

A função utiliza Python 3.12 e uma camada AWS SDK for pandas para disponibilizar Pandas e PyArrow.

### AWS Glue Data Catalog

Responsável por armazenar os metadados das tabelas, incluindo nomes das colunas, tipos de dados e localização dos arquivos no S3.

Banco de dados utilizado: `db_vendas`.

Tabelas cadastradas:

- `tb_vendas`: dados tratados sem particionamento.
- `tb_vendas_particionadas`: dados organizados por ano e mês.

### Amazon Athena

Responsável pela execução de consultas SQL diretamente sobre os arquivos Parquet armazenados no S3.

Permite realizar análises como faturamento total, vendas por categoria, faturamento por região e evolução mensal das vendas.

### Amazon CloudWatch

Utilizado para acompanhar as execuções da função Lambda, consultar logs e identificar possíveis falhas de processamento.

## 4. Organização dos dados no S3

**Bucket RAW**

```text
datalake-raw-bianca-oliveira-2026/
└── vendas/
    └── vendas.csv
```

**Bucket PROCESSED**

```text
datalake-processed-bianca-oliveira-2026/
├── vendas/
│   └── vendas.parquet
│
└── vendas_particionadas/
    └── ano=2026/
        ├── mes=01/
        │   └── dados.parquet
        ├── mes=02/
        │   └── dados.parquet
        └── mes=03/
            └── dados.parquet
```

## 5. Particionamento

Foi implementada uma estrutura de particionamento por ano e mês utilizando Python e Pandas.

As partições foram armazenadas no S3 seguindo o padrão Hive:

`ano=2026/mes=01/`

O particionamento permite que o Athena selecione somente os diretórios necessários quando as consultas utilizam filtros nas colunas de partição.

Essa abordagem pode reduzir o volume de dados lidos e melhorar a eficiência das consultas, especialmente em conjuntos de dados maiores.

O particionamento foi implementado no script Python local. A automação da atualização das partições pelo Lambda é uma melhoria futura.

## 6. Segurança e permissões

O projeto foi desenvolvido em um ambiente de laboratório AWS utilizando o Vocareum.

A função Lambda utiliza uma IAM Role existente, denominada `LabRole`, para acessar os recursos autorizados.

As credenciais temporárias utilizadas no ambiente local são mantidas em variáveis de ambiente e não devem ser versionadas no GitHub.

## 7. Monitoramento e validação

O processamento automatizado foi testado com um arquivo CSV contendo 100 registros.

O Lambda executou o processamento com sucesso e registrou os seguintes resultados:

- Registros recebidos: 100.
- Registros processados: 100.
- Tempo de execução: aproximadamente 646 ms.
- Memória máxima utilizada: 212 MB.
- Memória configurada: 512 MB.

O gatilho do S3 também foi validado por meio de uma nova execução registrada no CloudWatch após o upload de um arquivo CSV.

## 8. Limitações e melhorias futuras

A versão atual demonstra um pipeline funcional para fins de aprendizado e portfólio.

As próximas melhorias previstas incluem:

- Gerar nomes de arquivos Parquet dinâmicos para evitar sobrescritas.
- Automatizar a atualização das partições no Glue Data Catalog.
- Implementar tratamento de erros e validações adicionais.
- Adicionar testes automatizados.
- Criar mecanismos de monitoramento e alertas.
- Preparar a infraestrutura para ambientes além do laboratório Vocareum.

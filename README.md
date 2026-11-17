# AWS Sales Data Pipeline

Pipeline de Engenharia de Dados para processar vendas em CSV usando serviços AWS, com armazenamento em Parquet, catálogo de metadados e consultas SQL.

## Arquitetura

```text
CSV → S3 RAW → evento ObjectCreated → AWS Lambda (Python, Pandas, PyArrow)
                                       ↓
                                 S3 PROCESSED (Parquet)
                                       ↓
                               AWS Glue Data Catalog
                                       ↓
                                  Amazon Athena
```

O CloudWatch registra as execuções do Lambda. O projeto também inclui um processamento local em Python e um experimento de particionamento por ano e mês.

## Tecnologias

- Amazon S3: armazenamento RAW e PROCESSED
- AWS Lambda: processamento acionado por evento do S3
- Python, Boto3, Pandas e PyArrow: leitura, limpeza e conversão para Parquet
- AWS Glue Data Catalog: metadados das tabelas
- Amazon Athena: consultas SQL
- Amazon CloudWatch: logs e monitoramento

## Estrutura

```text
src/         # scripts Python
sql/         # criação de tabela e análises
 docs/        # detalhes da arquitetura
 data/        # dados fictícios opcionais
```

## Transformações

1. Leitura do CSV de vendas do S3 RAW.
2. Remoção de registros duplicados.
3. Remoção de registros sem campos obrigatórios.
4. Exclusão de linhas com quantidade ou valor unitário não positivos.
5. Conversão da data para tipo datetime.
6. Cálculo de `valor_total = quantidade * valor_unitario`.
7. Escrita em Parquet com compressão Snappy no S3 PROCESSED.

Colunas: `id_venda`, `data`, `produto`, `categoria`, `regiao`, `quantidade`, `valor_unitario`, `valor_total`.

## Execução local

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Configure suas credenciais AWS **localmente**, sem publicá-las no repositório. O script de exemplo utiliza as credenciais fornecidas pelo ambiente, incluindo variáveis carregadas de `.env` quando presente.

```bash
python src/processamento.py
```

## AWS Lambda

A função `processamento-vendas` foi testada com Python 3.12 e uma camada compatível com Pandas e PyArrow (`AWSSDKPandas-Python312`). O S3 RAW dispara a execução em eventos de criação de arquivos CSV no prefixo `vendas/`.

**Limitação da versão documentada:** o código de referência do Lambda lê o objeto fixo `vendas/vendas.csv` e sobrescreve `vendas/vendas.parquet`. O processamento dinâmico por nome de arquivo foi planejado, mas deve ser validado antes de ser descrito como concluído.

## Consultas SQL

Veja `sql/analises_vendas.sql`. Os metadados ficam no banco `db_vendas` do Glue, incluindo uma tabela regular (`tb_vendas`) e uma tabela particionada (`tb_vendas_particionadas`).

## Resultado do teste

Um teste do Lambda foi concluído com sucesso, processando 100 registros e enviando o Parquet ao S3 PROCESSED. A execução automática por evento S3 também foi confirmada em logs.

## Próximas melhorias

- Processar a chave do objeto recebida no evento do S3 e gerar destinos únicos.
- Automatizar a atualização das partições no catálogo.
- Adicionar testes e tratamento de erros.
- Incluir métricas de qualidade e custo.

## Segurança

Nunca inclua `.env`, chaves de acesso, tokens, credenciais de laboratório ou arquivos locais sensíveis no Git. Buckets e nomes de recursos nos scripts são exemplos da implementação e podem ser adaptados para outros ambientes.

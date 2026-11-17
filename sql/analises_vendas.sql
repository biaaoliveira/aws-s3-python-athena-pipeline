-- 1. Quantas vendas foram registradas?

SELECT
    COUNT(*) AS total_vendas
FROM db_vendas.tb_vendas;


-- 2. Qual é o faturamento total?

SELECT
    ROUND(SUM(valor_total), 2) AS faturamento_total
FROM db_vendas.tb_vendas;


-- 3. Quais categorias existem?

SELECT DISTINCT
    categoria
FROM db_vendas.tb_vendas;


-- 4. Qual é o faturamento por categoria?

SELECT
    categoria,
    COUNT(*) AS total_vendas,
    SUM(quantidade) AS unidades_vendidas,
    ROUND(SUM(valor_total), 2) AS faturamento_total
FROM db_vendas.tb_vendas
GROUP BY categoria
ORDER BY faturamento_total DESC;


-- 5. Qual região apresenta o maior faturamento?

SELECT
    regiao,
    ROUND(SUM(valor_total), 2) AS faturamento_total
FROM db_vendas.tb_vendas
GROUP BY regiao
ORDER BY faturamento_total DESC;


-- 6. Quais são os 3 produtos com maior faturamento?

SELECT
    produto,
    ROUND(SUM(valor_total), 2) AS faturamento_total
FROM db_vendas.tb_vendas
GROUP BY produto
ORDER BY faturamento_total DESC
LIMIT 3;


-- 7. Qual é o faturamento mensal?

SELECT
    YEAR(data) AS ano,
    MONTH(data) AS mes,
    ROUND(SUM(valor_total), 2) AS faturamento_total
FROM db_vendas.tb_vendas
GROUP BY YEAR(data), MONTH(data)
ORDER BY ano, mes;


-- 8. Qual é o preço unitário médio por categoria?

SELECT
    categoria,
    ROUND(AVG(valor_unitario), 2) AS preco_medio
FROM db_vendas.tb_vendas
GROUP BY categoria
ORDER BY preco_medio DESC;


-- 9. Quais regiões faturaram mais de R$ 5.000?

SELECT
    regiao,
    ROUND(SUM(valor_total), 2) AS faturamento_total
FROM db_vendas.tb_vendas
GROUP BY regiao
HAVING SUM(valor_total) > 5000
ORDER BY faturamento_total DESC;


-- 10. Qual é a participação percentual
-- de cada categoria no faturamento total?

SELECT
    categoria,
    ROUND(SUM(valor_total), 2) AS faturamento_categoria,
    ROUND(
        100.0 * SUM(valor_total)
        / SUM(SUM(valor_total)) OVER (),
        2
    ) AS percentual_faturamento
FROM db_vendas.tb_vendas
GROUP BY categoria
ORDER BY percentual_faturamento DESC;


-- 11. Consultar apenas janeiro de 2026
-- utilizando a tabela particionada

SELECT
    COUNT(*) AS total_vendas,
    ROUND(SUM(valor_total), 2) AS faturamento_janeiro
FROM db_vendas.tb_vendas_particionadas
WHERE ano = 2026
  AND mes = '01';

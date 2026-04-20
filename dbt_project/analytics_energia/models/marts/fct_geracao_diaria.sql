{{ config(materialized='table') }}

WITH geracao AS (
    SELECT * FROM {{ ref('stg_ons_geracao') }}
)

SELECT
    data_referencia,
    subsistema,
    SUM(megawatts_gerados) AS total_gerado_dia,
    COUNT(DISTINCT nome_usina) AS total_usinas_ativas
FROM geracao
WHERE status_operacional = 'Ativa'
GROUP BY 1, 2
ORDER BY 1 DESC
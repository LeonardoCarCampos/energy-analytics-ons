-- Aqui limpamos os dados brutos do ONS
WITH source AS (
    SELECT * FROM {{ source('raw_ons', 'geracao_usina_diaria') }}
),

renamed AS (
    SELECT
        SAFE_CAST(din_instante AS TIMESTAMP) AS data_referencia,
        LOWER(id_subsistema) AS subsistema,
        LOWER(nom_usina) AS nome_usina,
        val_geracao AS megawatts_gerados,
        -- Exemplo de lógica de negócio:
        CASE 
            WHEN val_geracao > 0 THEN 'Ativa'
            ELSE 'Inativa'
        END AS status_operacional
    FROM source
)

SELECT * FROM renamed
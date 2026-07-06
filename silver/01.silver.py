# Databricks notebook source
config = spark.table("anac.params.global_config").collect()[0]

silver_path = config["silver_path"]

# COMMAND ----------

df_silver = spark.sql("""                 
SELECT
    Aerodromo_de_Destino,
    Aerodromo_de_Origem,
    CLS,
    Categoria_da_Aeronave,
    `Classificacao_da_Ocorrência`,
    Danos_a_Aeronave,
    Data_da_Ocorrencia,
    Descricao_do_Tipo,
    Fase_da_Operacao,
    Historico,
    `Hora_da_Ocorrência`,
    ICAO,
    Ilesos_Passageiros,
    Ilesos_Tripulantes,
    Latitude,
    Lesoes_Desconhecidas_Passageiros,
    Lesoes_Desconhecidas_Terceiros,
    Lesoes_Desconhecidas_Tripulantes,
    Lesoes_Fatais_Passageiros,
    Lesoes_Fatais_Terceiros,
    Lesoes_Fatais_Tripulantes,
    Lesoes_Graves_Passageiros,
    Lesoes_Graves_Terceiros,
    Lesoes_Graves_Tripulantes,
    Lesoes_Leves_Passageiros,
    Lesoes_Leves_Terceiros,
    Lesoes_Leves_Tripulantes,
    Longitude,
    Matricula,
    Modelo,
    Municipio,
    Nome_do_Fabricante,
    Numero_da_Ficha,
    Numero_da_Ocorrencia,
    Numero_de_Assentos,
    Operacao,
    Operador,
    Operador_Padronizado,
    PMD,
    PSSO,
    Regiao,
    Tipo_ICAO,
    Tipo_de_Aerodromo,
    Tipo_de_Ocorrencia,
    UF
FROM anac.analytics.bronze_ocorrencia_ampla       
""")

# COMMAND ----------

from pyspark.sql.functions import col, when, coalesce, lit, length, trim

campos_int = [
    'Lesoes_Desconhecidas_Passageiros', 'Lesoes_Desconhecidas_Terceiros', 'Lesoes_Desconhecidas_Tripulantes', 
    'Lesoes_Fatais_Passageiros', 'Lesoes_Fatais_Terceiros', 'Lesoes_Fatais_Tripulantes', 
    'Lesoes_Graves_Passageiros', 'Lesoes_Graves_Terceiros', 'Lesoes_Graves_Tripulantes', 
    'Lesoes_Leves_Passageiros', 'Lesoes_Leves_Terceiros', 'Lesoes_Leves_Tripulantes', 
    'Ilesos_Tripulantes', 'Ilesos_Passageiros'
]

campos_string = [
    coluna for coluna, tipo in df_silver.dtypes 
    if tipo == 'string' and coluna not in campos_int
]

regra_int = {
    campo: coalesce(col(campo).cast("int"), lit(0)) 
    for campo in campos_int
}

regra_null = {
    campo: when(col(campo).isNull() | 
                (col(campo) == '-') | 
                (length(trim(col(campo))) == 0), 'Não informado').otherwise(col(campo))
    for campo in campos_string
}

regras = {**regra_int, **regra_null}

df_silver = df_silver.withColumns(regras)

# COMMAND ----------

df_silver.write \
    .mode("overwrite") \
    .format("delta") \
    .option("mergeSchema", "true") \
    .save(f'{silver_path}' + "ocorrencia_ampla")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS anac.analytics.silver_ocorrencia_ampla
# MAGIC
# MAGIC LOCATION 'abfss://anac@lfbazure.dfs.core.windows.net/silver/ocorrencia_ampla';

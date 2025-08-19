# Databricks notebook source
# MAGIC %md
# MAGIC # Feature POC - Gold Layer
# MAGIC Agregaciones y métricas finales para el POC

# COMMAND ----------

# Importar librerías necesarias
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder.appName("Feature_POC_Gold").getOrCreate()

# COMMAND ----------

# Leer datos de Silver layer
df_silver = spark.table("silver.uc_banner_pers")

print(f"Registros en Silver: {df_silver.count()}")
display(df_silver.limit(10))

# COMMAND ----------

# Transformaciones Gold - Agregaciones y métricas
df_gold = df_silver.groupBy("some_category_field").agg(
    count("*").alias("total_records"),
    countDistinct("some_id_field").alias("unique_ids"),
    max("processed_at").alias("last_processed")
).withColumn(
    "calculation_timestamp", 
    current_timestamp()
)

# COMMAND ----------

# Guardar en Gold layer
df_gold.write.mode("overwrite").saveAsTable("gold.feature_poc_metrics")

print(f"Métricas calculadas: {df_gold.count()}")
display(df_gold)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resultados del POC
# MAGIC - Datos procesados exitosamente a través de las 3 capas (Bronze -> Silver -> Gold)
# MAGIC - Métricas calculadas y disponibles para análisis
# MAGIC - Pipeline funcional para benjamin.vergara@uc.cl
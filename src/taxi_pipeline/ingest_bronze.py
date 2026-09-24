# Databricks notebook source
"""Ingestão bronze: lê o Parquet da landing e grava Delta, sem regra de negócio.

Roda como notebook Databricks (job serverless). Adiciona apenas metadados de
ingestão: _ingested_at, _source e _batch_id.
"""

# COMMAND ----------

import uuid
from datetime import UTC, datetime

import yaml
from pyspark.sql import functions as F

# COMMAND ----------

with open("../../conf/config.yaml") as f:
    config = yaml.safe_load(f)

catalog = config["catalog"]
volume_path = config["source"]["volume_path"]
file_name = config["source"]["file_name"]
target_schema = config["target"]["schema"]
target_table = config["target"]["table"]

source_path = f"{volume_path}/{file_name}"
target = f"{catalog}.{target_schema}.{target_table}"

batch_id = str(uuid.uuid4())
ingested_at = datetime.now(UTC)

# COMMAND ----------

df = spark.read.parquet(source_path)  # noqa: F821  # spark é injetado pelo runtime do Databricks

df_bronze = (
    df.withColumn("_ingested_at", F.lit(ingested_at))
    .withColumn("_source", F.lit(file_name))
    .withColumn("_batch_id", F.lit(batch_id))
)

# COMMAND ----------

df_bronze.write.format("delta").mode("overwrite").saveAsTable(target)

print(f"{df_bronze.count()} linhas gravadas em {target} (batch_id={batch_id})")
#!/usr/bin/env python3
"""
JDBC → Delta Test

Liest eine Demo-Abfrage aus der im Compose-Stack laufenden Postgres-Datenbank
und schreibt das Ergebnis als Delta-Tabelle auf das lokale Dateisystem.
Anschließend werden Zeilen gezählt und die History angezeigt, um zu
verifizieren, dass es sich um eine echte Delta-Tabelle handelt.
"""
from pyspark.sql import SparkSession

# ---------------------------------------------------------------------------
# Spark-Session mit Delta-Support starten
# ---------------------------------------------------------------------------

builder = (
    SparkSession.builder.appName("JDBC → Delta Test")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

spark = builder.getOrCreate()

# ---------------------------------------------------------------------------
# Daten via JDBC lesen
# ---------------------------------------------------------------------------

jdbc_url = "jdbc:postgresql://postgres:5432/metastore_db"  # Service-Name gem. Compose
query = "(select 1 as id, 'hello via jdbc' as txt) as src"  # demo-Select ohne Tabelle

jdbc_df = (
    spark.read.format("jdbc")
    .option("url", jdbc_url)
    .option("dbtable", query)
    .option("user", "admin")
    .option("password", "admin")
    .load()
)
print("=== JDBC-Daten ===")
jdbc_df.show(truncate=False)

# ---------------------------------------------------------------------------
# Als Delta schreiben
# ---------------------------------------------------------------------------

delta_path = "file:///opt/spark-apps/delta-warehouse/jdbc_demo"  # Container-Pfad

jdbc_df.write.format("delta").mode("overwrite").save(delta_path)
print("✅ Delta-Tabelle geschrieben →", delta_path)

# ---------------------------------------------------------------------------
# Verifikation – zählen & History – beweist echten Delta-Log
# ---------------------------------------------------------------------------

from delta.tables import DeltaTable

delta_tbl = DeltaTable.forPath(spark, delta_path)
print("👀 Delta-Zeilen:", delta_tbl.toDF().count())

delta_tbl.history().show(truncate=False)

spark.stop() 
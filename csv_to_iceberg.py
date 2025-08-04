#!/usr/bin/env python3
"""
Spark-Skript zur Ingestion einer CSV-Datei in eine Iceberg-Tabelle und Anzeige der ersten Zeilen.
"""

from pyspark.sql import SparkSession

if __name__ == "__main__":
    # Spark-Session mit Iceberg-Konfiguration erstellen
    spark = SparkSession.builder \
        .appName("CSV to Iceberg Table") \
        .config("spark.sql.catalog.iceberg", "org.apache.iceberg.spark.SparkCatalog") \
        .config("spark.sql.catalog.iceberg.catalog-impl", "org.apache.iceberg.jdbc.JdbcCatalog") \
        .config("spark.sql.catalog.iceberg.uri", "jdbc:postgresql://metastore:5432/iceberg?user=postgres-user&password=postgres-password") \
        .config("spark.sql.catalog.iceberg.warehouse", "s3a://wba/warehouse") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://object-store:9000") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.access.key", "minio-user") \
        .config("spark.hadoop.fs.s3a.secret.key", "minio-password") \
        .getOrCreate()

    # Pfad zur CSV-Datei
    input_csv = "delta/test-data/Testdaten.csv"
    # CSV einlesen
    df = spark.read.option("header", True).option("inferSchema", True).csv(input_csv)

    # Iceberg-Tabelle schreiben (Parquet-Format)
    df.writeTo("iceberg.default.testdaten").using("parquet").createOrReplace()

    # Vorschau der ersten 10 Zeilen
    spark.sql("SELECT * FROM iceberg.default.testdaten LIMIT 10").show(truncate=False)

    spark.stop() 
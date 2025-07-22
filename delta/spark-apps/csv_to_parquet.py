#!/usr/bin/env python3
"""
CSV zu Parquet Konvertierung
Konvertiert eine CSV-Datei in Parquet, damit Apache Iceberg oder Spark sie ohne zusätzlichen Connector verwenden können.
"""
from pyspark.sql import SparkSession
import os

def main():
    # Spark Session erstellen
    spark = SparkSession.builder \
        .appName("CSV zu Parquet") \
        .getOrCreate()

    # Pfad zur CSV-Datei (Testdaten.csv im Arbeitsverzeichnis delta/spark-apps/test-data)
    input_path = os.environ.get("CSV_INPUT_PATH", "/opt/spark-apps/test-data/Testdaten.csv")
    # Zielverzeichnis für Parquet-Datei
    output_path = os.environ.get("PARQUET_OUTPUT_PATH", "/opt/spark-apps/parquet/Testdaten.parquet")

    # CSV einlesen
    df = spark.read \
        .option("header", True) \
        .option("inferSchema", True) \
        .csv(input_path)

    # Als Parquet speichern
    df.write \
        .mode("overwrite") \
        .option("compression", "snappy") \
        .parquet(output_path)

    print("Anzahl Zeilen geschrieben:", spark.read.parquet(output_path).count())

    spark.stop()

if __name__ == "__main__":
    main() 
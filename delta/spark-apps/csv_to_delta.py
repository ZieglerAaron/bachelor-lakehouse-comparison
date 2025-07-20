#!/usr/bin/env python3
"""
CSV to Delta Lake Konvertierung
Beispiel-Anwendung für Delta Lake Stack
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
from delta.tables import DeltaTable
import os

def create_spark_session():
    """Erstellt eine Spark Session mit Delta Lake Konfiguration"""
    return SparkSession.builder \
        .appName("CSV to Delta Lake") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()

def create_sample_csv_data(spark):
    """Erstellt Beispieldaten im CSV-Format"""
    print("📝 Erstelle Beispieldaten...")
    
    # Schema definieren
    schema = StructType([
        StructField("id", IntegerType(), False),
        StructField("name", StringType(), True),
        StructField("department", StringType(), True),
        StructField("salary", IntegerType(), True),
        StructField("created_at", TimestampType(), True)
    ])
    
    # Beispieldaten
    data = [
        (1, "Max Mustermann", "IT", 50000, "2024-01-01 09:00:00"),
        (2, "Anna Schmidt", "HR", 45000, "2024-01-01 10:00:00"),
        (3, "Tom Weber", "Sales", 48000, "2024-01-01 11:00:00"),
        (4, "Lisa Müller", "IT", 52000, "2024-01-01 12:00:00"),
        (5, "Paul Fischer", "Marketing", 46000, "2024-01-01 13:00:00")
    ]
    
    # DataFrame erstellen
    df = spark.createDataFrame(data, schema)
    
    # Als CSV speichern
    df.write.mode("overwrite").csv("s3a://delta/input/employees.csv", header=True)
    print("✅ Beispieldaten erstellt: s3a://delta/input/employees.csv")
    
    return df

def csv_to_delta_conversion(spark):
    """Konvertiert CSV-Daten zu Delta-Format"""
    print("🔄 Starte CSV zu Delta Konvertierung...")
    
    # CSV-Daten lesen
    df = spark.read.csv("s3a://delta/input/employees.csv", header=True, inferSchema=True)
    
    print(f"📊 CSV-Daten gelesen: {df.count()} Zeilen")
    df.show()
    
    # Als Delta-Format speichern
    df.write.format("delta").mode("overwrite").save("s3a://delta/output/employees_delta")
    print("✅ Delta-Tabelle erstellt: s3a://delta/output/employees_delta")
    
    # Delta-Tabelle lesen und anzeigen
    delta_df = spark.read.format("delta").load("s3a://delta/output/employees_delta")
    print("📊 Delta-Tabelle Inhalt:")
    delta_df.show()
    
    return delta_df

def demonstrate_delta_features(spark):
    """Demonstriert Delta Lake Features"""
    print("🚀 Demonstriere Delta Lake Features...")
    
    # Delta-Tabelle laden
    delta_table = DeltaTable.forPath(spark, "s3a://delta/output/employees_delta")
    
    # Neue Daten hinzufügen
    new_data = [
        (6, "Sarah Klein", "Finance", 49000, "2024-01-02 09:00:00"),
        (7, "Michael Bauer", "IT", 53000, "2024-01-02 10:00:00")
    ]
    
    new_df = spark.createDataFrame(new_data, ["id", "name", "department", "salary", "created_at"])
    
    # Merge-Operation (Upsert)
    delta_table.alias("target").merge(
        new_df.alias("source"),
        "target.id = source.id"
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    
    print("✅ Neue Daten hinzugefügt (Merge-Operation)")
    
    # Aktualisierte Tabelle anzeigen
    updated_df = spark.read.format("delta").load("s3a://delta/output/employees_delta")
    print("📊 Aktualisierte Delta-Tabelle:")
    updated_df.show()
    
    # Version-Historie anzeigen
    print("📋 Delta-Tabelle Versionen:")
    delta_table.history().show()

def main():
    """Hauptfunktion"""
    print("🎯 Delta Lake CSV to Delta Konvertierung")
    print("=" * 50)
    
    # Spark Session erstellen
    spark = create_spark_session()
    
    try:
        # Beispieldaten erstellen
        create_sample_csv_data(spark)
        
        # CSV zu Delta Konvertierung
        csv_to_delta_conversion(spark)
        
        # Delta Features demonstrieren
        demonstrate_delta_features(spark)
        
        print("\n✅ Alle Operationen erfolgreich abgeschlossen!")
        print("\n🔗 MinIO Web UI: http://localhost:9001")
        print("   Username: minioadmin")
        print("   Password: minioadmin")
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()

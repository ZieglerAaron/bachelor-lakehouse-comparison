#!/usr/bin/env python3
"""
Echter Delta Lake Test - Mit bereinigten Spaltennamen
"""
from pyspark.sql import SparkSession
from delta.tables import DeltaTable
from pyspark.sql.functions import col

def main():
    # Spark Session ohne V2-Extensions: nur V1 Delta-API
    spark = SparkSession.builder \
        .appName("Real Delta Lake Test - Fixed") \
        .config("spark.sql.warehouse.dir", "file:///opt/spark-apps/delta-warehouse") \
        .getOrCreate()

    print("=== ECHTER DELTA LAKE TEST (FIXED) ===")
    
    # CSV einlesen
    csv_file = "file:///opt/spark-apps/test-data/Testdaten.csv"
    print(f"1. CSV einlesen von: {csv_file}")
    
    df = spark.read.option("header", True).option("inferSchema", True).csv(csv_file)
    print(f"   Eingelesene Zeilen: {df.count()}")
    
    # PROBLEM: Delta Lake mag keine Leerzeichen in Spaltennamen!
    print("2. Spaltennamen bereinigen (Delta Lake Requirement):")
    original_columns = df.columns
    print(f"   Originale Spalten: {original_columns}")
    
    # Leerzeichen durch Unterstriche ersetzen
    clean_columns = [col_name.replace(" ", "_") for col_name in original_columns]
    print(f"   Bereinigte Spalten: {clean_columns}")
    
    # DataFrame mit bereinigten Spaltennamen
    df = df.toDF(*[c.replace(" ", "_") for c in df.columns])
    print("   Spaltennamen bereinigt")
    
    # ECHTER Delta Lake Table (jetzt mit kompatiblen Spaltennamen!)
    delta_table_path = "file:///opt/spark-apps/delta-warehouse/testdaten_delta_fixed"
    print(f"3. Delta Table erstellen: {delta_table_path}")
    
    # Als Delta Table schreiben
    df.write \
        .format("delta") \
        .mode("overwrite") \
        .save(delta_table_path)
    
    print("   Delta Table erstellt")
    
    # Verifikation: Als Delta Table lesen
    print("4. Delta Table Verifikation:")
    delta_df = spark.read.format("delta").load(delta_table_path)
    print(f"   Delta Table Zeilen: {delta_df.count()}")
    
    # Delta Table Metadaten prüfen
    print("5. Delta Table Metadaten:")
    delta_table = DeltaTable.forPath(spark, delta_table_path)
    history = delta_table.history()
    print("   Delta History:")
    history.select("version", "timestamp", "operation", "operationMetrics").show(truncate=False)
    
    # SQL-Interface testen
    print("6. SQL Interface Test:")
    delta_df.createOrReplaceTempView("testdaten")
    result = spark.sql("SELECT COUNT(*) as total_rows FROM testdaten")
    result.show()
    
    spark.stop()
    
    print("\n=== DELTA LAKE FUNKTIONEN ===")
    print("Delta Table Format")
    print("ACID Transaktionen")
    print("Time Travel (History)")
    print("SQL Interface")
    print("Schema Evolution bereit")
    print("\n=== HINWEISE ZUR KOMPLEXITÄT ===")
    print("JAR-Management erforderlich")
    print("Schema-Einschränkungen (keine Leerzeichen)")
    print("Mehr Setup als nur Parquet")

if __name__ == "__main__":
    main() 
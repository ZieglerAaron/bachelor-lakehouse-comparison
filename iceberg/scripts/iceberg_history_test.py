from pyspark.sql import SparkSession

if __name__ == "__main__":
    # SparkSession mit Iceberg-Catalog konfigurieren
    spark = SparkSession.builder \
        .appName("IcebergHistoryTest") \
        .master("local[*]") \
        .config("spark.sql.catalog.local_iceberg", "org.apache.iceberg.spark.SparkCatalog") \
        .config("spark.sql.catalog.local_iceberg.type", "hadoop") \
        .config("spark.sql.catalog.local_iceberg.warehouse", "file:///tmp/iceberg_warehouse") \
        .getOrCreate()

    # Log-Level auf ERROR setzen
    spark.sparkContext.setLogLevel("ERROR")

    # Beispiel-Daten erzeugen
    data = [(1, "Alice"), (2, "Bob")]
    df = spark.createDataFrame(data, ["id", "name"])

    # Tabelle erstellen oder ersetzen und initiale Daten schreiben
    df.writeTo("local_iceberg.default.iceberg_test").createOrReplace()

    # Beispieländerung: Datensatz mit id=1 löschen
    spark.sql("DELETE FROM local_iceberg.default.iceberg_test WHERE id = 1")

    # Historie der Iceberg-Tabelle ausgeben
    print("=== Iceberg History ===")
    spark.sql("SELECT * FROM local_iceberg.default.iceberg_test.history").show(truncate=False)

    # Ersten Snapshot ermitteln für Time Travel
    first_snapshot = spark.sql(
        "SELECT snapshot_id FROM local_iceberg.default.iceberg_test.history ORDER BY made_current_at LIMIT 1"
    ).collect()[0][0]

    # Time Travel: Zustand zum ersten Snapshot auslesen
    print(f"=== Time Travel: Snapshot {first_snapshot} ===")
    spark.read.format("iceberg") \
        .option("snapshot-id", first_snapshot) \
        .load("local_iceberg.default.iceberg_test") \
        .show(truncate=False)

    spark.stop()
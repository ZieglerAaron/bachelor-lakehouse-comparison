from pyspark.sql import SparkSession

if __name__ == "__main__":
    # SparkSession mit Delta-Unterstützung initialisieren
    spark = SparkSession.builder \
        .appName("DeltaHistoryTest") \
        .master("local[*]") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    # Log-Level auf ERROR setzen, um Info-Logs zu unterdrücken
    spark.sparkContext.setLogLevel("ERROR")

    # DataFrame mit Beispiel-Daten erzeugen
    data = [(1, "Lufthansa"), (2, "Aeroflot")]
    df = spark.createDataFrame(data, ["id", "airline"])

    # Delta-Tabelle im Verzeichnis file:///tmp/delta_test im Overwrite-Modus speichern
    df.write.format("delta").mode("overwrite").save("file:///tmp/delta_test")

    # Tabelle für SQL-Abfragen registrieren
    spark.sql("DROP TABLE IF EXISTS delta_test")
    spark.sql("CREATE TABLE delta_test USING delta LOCATION 'file:///tmp/delta_test'")

    # Beispieländerung: Aktualisieren des Namens für id=1
    spark.sql("""UPDATE delta_test SET airline = 'Lufthansa_updated' WHERE id = 1""")

    # Historie der Tabelle ausgeben
    print("=== Delta History ===")
    spark.sql("""DESCRIBE HISTORY delta_test""").show(truncate=False)

    # Time Travel: Zustand der Tabelle zu Version 0 anzeigen
    print("=== Time Travel: Version 0 ===")
    spark.read.format("delta") \
        .option("versionAsOf", 0) \
        .load("file:///tmp/delta_test") \
        .show(truncate=False)

    # SparkSession beenden
    spark.stop()
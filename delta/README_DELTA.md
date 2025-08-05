# Delta Lake Stack

Dieser Stack implementiert Delta Lake mit Apache Spark, Hive Metastore und MinIO.

## Komponenten

- **Apache Spark**: Distributed Computing Engine
- **Delta Lake**: ACID Table Format
- **Hive Metastore**: Metadata Management
- **MinIO**: Object Storage (S3-kompatibel)

## Schnellstart

### 1. Stack starten
```bash
docker compose up -d
```

### 2. JARs kopieren (falls benötigt)
```bash
# Delta Lake JARs in hive-config/ und spark-config/ kopieren
# Siehe Setup-Anweisungen unten
```

### 3. Spark-Anwendung ausführen
```bash
spark-submit --master spark://localhost:7077 \
  --packages io.delta:delta-core_2.12:2.4.0 \
  spark-apps/csv_to_delta.py
```

## Konfiguration

### Hive Metastore
Die Hive-Konfiguration befindet sich in `hive-config/hive-site.xml`.

### Spark Configuration
Die Spark-Konfiguration befindet sich in `spark-config/spark-defaults.conf`.

### MinIO Credentials
- Access Key: `minioadmin`
- Secret Key: `minioadmin`
- Endpoint: `http://localhost:9000`

## Beispiel-Anwendungen

### CSV zu Delta Konvertierung (Original-Repo)
Die Datei `spark-apps/csv_to_delta.py` aus dem Original-Repo zeigt eine einfache CSV-zu-Delta-Konvertierung:

```python
from delta.tables import DeltaTable
from pyspark.sql import SparkSession

def main():
    source_bucket = "wba"
    
    spark = SparkSession.builder \
        .appName("CSV File to Delta Lake Table") \
        .enableHiveSupport() \
        .getOrCreate()

    input_path = f"s3a://{source_bucket}/test-data/people-100.csv"
    delta_path = f"s3a://{source_bucket}/delta/wba/tables/"

    # Datenbank erstellen und verwenden
    spark.sql("CREATE DATABASE IF NOT EXISTS wba")
    spark.sql("USE wba")

    # CSV lesen und als Delta speichern
    df = spark.read.csv(input_path, header=True, inferSchema=True)
    df.write.format("delta").option("delta.columnMapping.mode", "name")\
        .option("path", f'{delta_path}/test_table')\
        .saveAsTable("wba.test_table")

if __name__ == "__main__":
    main()
```

### Erweiterte CSV zu Delta Konvertierung
Die Datei `spark-apps/csv_to_delta.py` (unser erweitertes Beispiel) zeigt zusätzliche Delta Lake Features:

```python
# Siehe die vollständige Implementierung in der Datei
# - Beispieldaten erstellen
# - CSV zu Delta Konvertierung
# - Delta Lake Features demonstrieren (Merge-Operationen, Versionierung)
```

## Test-Daten

Das Verzeichnis `test-data/` enthält Beispieldaten aus dem Original-Repo:
- `people-100.csv`: 100 Beispieldatensätze für Tests

## MinIO Web UI

Zugriff über: http://localhost:9001
- Username: `minioadmin`
- Password: `minioadmin`

## Test-Datenhistorie und Audit

Ein einfaches Testskript `delta_history_test.py` im Verzeichnis `spark-apps` erstellt eine kleine Delta-Tabelle, führt eine Änderung durch und gibt die Versionierungs-Historie mit DESCRIBE HISTORY aus:

```bash
spark-submit /Users/aaron/UniAufMac/Bachelor/bachelor-lakehouse-comparison/delta/spark-apps/delta_history_test.py
```

Die Ausgabe zeigt die Spalten `version`, `timestamp`, `userId`, `operation` und `operationMetrics`, anhand derer man jeden Commit nachvollziehen kann.

## Setup-Anweisungen

### Delta Lake JARs
Lade die folgenden JARs herunter und platziere sie in den entsprechenden Verzeichnissen:

1. `delta-core_2.12-2.4.0.jar` → `hive-config/`
2. `delta-core_2.12-2.4.0.jar` → `spark-config/`

### Spark Submit mit JARs
```bash
spark-submit \
  --master spark://localhost:7077 \
  --jars spark-config/delta-core_2.12-2.4.0.jar \
  --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
  --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
  spark-apps/csv_to_delta.py
```

## Dateien aus dem Original-Repo

- `docker-compose.yml.original`: Ursprüngliche Docker Compose-Konfiguration mit erweiterten Services
- `Dockerfile`: Custom Dockerfile für Hive Metastore
- `hive-config/`: Erweiterte Hive-Konfigurationen
- `spark-config/`: Erweiterte Spark-Konfigurationen
- `spark-apps/csv_to_delta.py`: Einfache CSV-zu-Delta-Konvertierung
- `test-data/`: Beispieldaten für Tests

## Troubleshooting

### Container-Logs anzeigen
```bash
docker compose logs -f
```

### Stack stoppen
```bash
docker compose down
```

### Stack mit Volumes löschen
```bash
docker compose down -v
```

### Spark UI
Zugriff über: http://localhost:4040 (während Spark-Job läuft)

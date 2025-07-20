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

## Beispiel-Anwendung

### CSV zu Delta Konvertierung
Die Datei `spark-apps/csv_to_delta.py` zeigt, wie CSV-Daten in Delta-Format konvertiert werden.

```python
from pyspark.sql import SparkSession
from delta.tables import DeltaTable

# Spark Session mit Delta Lake
spark = SparkSession.builder \
    .appName("CSV to Delta") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# CSV lesen
df = spark.read.csv("s3a://delta/input/sample.csv", header=True)

# Als Delta schreiben
df.write.format("delta").mode("overwrite").save("s3a://delta/output/sample_delta")
```

## MinIO Web UI

Zugriff über: http://localhost:9001
- Username: `minioadmin`
- Password: `minioadmin`

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

# Apache Iceberg: Ingestion- und Monitoring-Tests

Dieser Ordner beschreibt die Iceberg-spezifischen Tests und das notwendige Setup.

## Komponenten

- Trino (SQL Engine)
- Apache Iceberg (Table Format)
- PostgreSQL (Metastore)
- MinIO (Object Storage, S3-kompatibel)

## Setup

1) Stack starten
```bash
docker compose up -d
```

2) Basissetup ausführen (Schema/Tabelle/Datenbeispiele)
```bash
./scripts/iceberg-setup.sh
```

3) Trino CLI öffnen
```bash
docker exec -it iceberg-trino-1 trino
```

## Ingestion-Test (CSV via Spark, Abfrage via Trino)

- Script: `csv_to_iceberg.py` (Projektwurzel)
- Voraussetzungen: laufender Iceberg-Stack
- Ausführung (Beispiel):
```bash
docker run --network lakehouse bitnami/spark:3.2 \
  spark-submit --master 'local[*]' \
  --packages org.apache.iceberg:iceberg-spark-runtime-3.2_2.12:1.1.0,org.postgresql:postgresql:42.5.4 \
  /workspace/bachelor-lakehouse-comparison/csv_to_iceberg.py
```

- Verifikation (Trino):
```sql
SELECT * FROM iceberg.default.testdaten LIMIT 20;
```

## Monitoring-/Audit-Test (History, Time Travel)

- Script: `delta/spark-apps/iceberg_history_test.py`
- Ablauf:
  - Tabelle schreiben, Datensatz löschen
  - Historie über Metadata-Table `...history` anzeigen
  - Snapshot-ID ermitteln und früheren Zustand lesen
- Ausführung (Beispiel):
```bash
spark-submit delta/spark-apps/iceberg_history_test.py
```

## Konfiguration

- Iceberg-Katalog: `etc/catalog/iceberg.properties`
- MinIO Endpunkt: `http://localhost:9000`

## Troubleshooting

- Logs ansehen: `docker compose logs -f`
- Stack stoppen: `docker compose down`
- Stack inkl. Volumes löschen: `docker compose down -v`

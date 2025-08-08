# Bachelor Lakehouse Comparison: Ingestion- und Monitoring-Tests

Dieses Repository enthält zwei zentrale Testkategorien:

1) Ingestion-Tests (CSV/JDBC) für Apache Iceberg und Delta Lake
2) Monitoring-/Audit-Tests (History/Time Travel) für Delta Lake und Iceberg

## Ingestion-Tests

### Apache Iceberg (CSV über Spark, Abfrage über Trino)
- Script: `csv_to_iceberg.py`
- Setup: `cd iceberg && docker compose up -d`
- Ausführung (Beispiel):
```bash
docker run --network lakehouse bitnami/spark:3.2 \
  spark-submit --master 'local[*]' \
  --packages org.apache.iceberg:iceberg-spark-runtime-3.2_2.12:1.1.0,org.postgresql:postgresql:42.5.4 \
  csv_to_iceberg.py
```
- Verifikation per SQL (Trino CLI):
```sql
SELECT * FROM iceberg.default.testdaten LIMIT 20;
```

### Delta Lake (CSV über Spark)
- Script: `delta/spark-apps/csv_to_delta.py`
- Ausführung (Beispiel):
```bash
spark-submit --master spark://localhost:7077 \
  --packages io.delta:delta-core_2.12:2.4.0 \
  delta/spark-apps/csv_to_delta.py
```

### JDBC → Delta Lake (Demo)
- Script: `delta/spark-apps/jdbc_to_delta.py`
- Demonstriert JDBC-Quelle und Verifikation über Delta-History.

## Monitoring-/Audit-Tests (History, Time Travel)

### Delta Lake History/Time Travel
- Script: `delta/spark-apps/delta_history_test.py`
- Führt Update-Operation aus und zeigt `DESCRIBE HISTORY`; liest Version `versionAsOf=0`.

### Iceberg History/Time Travel
- Script: `delta/spark-apps/iceberg_history_test.py`
- Löscht Datensatz, zeigt Metadata-Table `...history`, liest mittels `snapshot-id` einen früheren Zustand.

## Projektstruktur (Auszug)
```
Tests/Heterogene Quellen ingestieren/
├── csv_ingest_iceberg.sql
└── README

delta/
└── spark-apps/
    ├── csv_to_delta.py
    ├── jdbc_to_delta.py
    ├── delta_history_test.py
    └── iceberg_history_test.py

iceberg/
└── scripts/
    └── iceberg-setup.sh
```

## Hinweise
- Nicht benötigte Minimal-/Performance-Skripte wurden entfernt.
- Alle Ausgaben und Dokumentation sind neutral formuliert (ohne Emojis/Emoticons).

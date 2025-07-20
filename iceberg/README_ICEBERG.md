# Apache Iceberg Stack

Dieser Stack implementiert Apache Iceberg mit Trino, PostgreSQL und MinIO.

## Komponenten

- **Trino**: SQL Query Engine
- **Apache Iceberg**: Table Format
- **PostgreSQL**: Metastore
- **MinIO**: Object Storage (S3-kompatibel)

## Schnellstart

### 1. Stack starten
```bash
docker compose up -d
```

### 2. Setup ausführen
```bash
./scripts/iceberg-setup.sh
```

### 3. Trino CLI verbinden
```bash
docker exec -it iceberg-trino-1 trino
```

## Konfiguration

### Iceberg Catalog
Die Iceberg-Konfiguration befindet sich in `etc/catalog/iceberg.properties`.

### MinIO Credentials
- Access Key: `minioadmin`
- Secret Key: `minioadmin`
- Endpoint: `http://localhost:9000`

## Beispiel-Queries

### Tabelle erstellen
```sql
CREATE SCHEMA IF NOT EXISTS iceberg.iceberg;
CREATE TABLE iceberg.iceberg.sample_table (
    id BIGINT,
    name VARCHAR,
    created_at TIMESTAMP
) WITH (
    format = 'PARQUET',
    location = 's3a://iceberg/'
);
```

### Daten einfügen
```sql
INSERT INTO iceberg.iceberg.sample_table VALUES 
(1, 'Test 1', TIMESTAMP '2024-01-01 10:00:00'),
(2, 'Test 2', TIMESTAMP '2024-01-01 11:00:00');
```

### Daten abfragen
```sql
SELECT * FROM iceberg.iceberg.sample_table;
```

## MinIO Web UI

Zugriff über: http://localhost:9001
- Username: `minioadmin`
- Password: `minioadmin`

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

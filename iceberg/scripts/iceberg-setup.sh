#!/bin/bash

# Iceberg Setup Script
# Führt grundlegende SQL-Befehle zur Initialisierung des Iceberg-Stacks aus

echo "Iceberg Stack Setup wird gestartet..."

# Warte auf Trino-Service
echo "Warte auf Trino-Service..."
sleep 30

# Verbinde zu Trino und führe Setup-Befehle aus
echo "Führe Iceberg-Setup aus..."

docker exec -i iceberg-controller-1 trino << 'EOF'

-- Schema erstellen
CREATE SCHEMA IF NOT EXISTS example.iceberg;

-- Beispiel-Tabelle erstellen
CREATE TABLE IF NOT EXISTS example.iceberg.sample_table (
    id BIGINT,
    name VARCHAR,
    created_at TIMESTAMP
) WITH (
    format = 'PARQUET',
    location = 's3://warehouse/sample_table/'
);

-- Test-Daten einfügen
INSERT INTO example.iceberg.sample_table VALUES 
(1, 'Test Datensatz 1', TIMESTAMP '2024-01-01 10:00:00'),
(2, 'Test Datensatz 2', TIMESTAMP '2024-01-01 11:00:00'),
(3, 'Test Datensatz 3', TIMESTAMP '2024-01-01 12:00:00');

-- Tabellen auflisten
SHOW TABLES FROM example.iceberg;

-- Test-Query ausführen
SELECT * FROM example.iceberg.sample_table;

EOF

echo "Iceberg Setup abgeschlossen."
echo ""
echo "MinIO Web UI: http://localhost:9001"
echo "   Username: minioadmin"
echo "   Password: minioadmin"
echo ""
echo "Trino CLI: docker exec -it iceberg-controller-1 trino"

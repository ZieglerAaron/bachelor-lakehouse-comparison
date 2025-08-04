-- csv_ingest_iceberg.sql
-- Ingestiert Testdaten.csv aus MinIO in eine Iceberg-Tabelle
CREATE TABLE IF NOT EXISTS example.iceberg.taxi_file
WITH (
  format = 'PARQUET'
) AS
SELECT *
FROM read_csv('s3a://iceberg/Testdaten.csv');

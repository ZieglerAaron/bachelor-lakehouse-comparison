# BA: Vergleich Apache Iceberg vs. Delta Lake

Dieses Repo enthält zwei vollständig getrennte Stacks:

- `iceberg/`  
  - Trino + Iceberg + Postgres + MinIO  
  - DDL/DML/Query-Beispiele  
  - Anleitung in `README_ICEBERG.md`

- `delta/`  
  - Spark + Delta + Hive Metastore + MinIO  
  - CSV-to-Delta Beispiel  
  - Anleitung in `README_DELTA.md`

## Schnellstart

### Repository klonen
```bash
git clone git@github.com:<dein-user>/bachelor-lakehouse-comparison.git
cd bachelor-lakehouse-comparison
```

### Automatisches Setup
```bash
./setup.sh
```
Das Setup-Script führt dich durch die Einrichtung und startet die gewünschten Stacks.

### Manuelles Setup

#### Iceberg Stack starten
```bash
cd iceberg
docker compose up -d
# danach: ./scripts/iceberg-setup.sh (oder SQL-Befehle aus README_ICEBERG.md)
```

#### Delta Lake Stack starten
```bash
cd delta
docker compose up -d
# ggf. JARs in hive-config und spark-config kopieren (siehe README_DELTA.md)
# dann: spark-submit für csv_to_delta.py
```

## Projektstruktur

```
bachelor-lakehouse-comparison/
│
├── README.md
├── setup.sh
├── .gitignore
│
├── iceberg/
│   ├── docker-compose.yml
│   ├── etc/
│   │   └── catalog/iceberg.properties
│   ├── scripts/
│   │   └── iceberg-setup.sh
│   └── README_ICEBERG.md
│
└── delta/
    ├── docker-compose.yml
    ├── hive-config/
    │   └── hive-site.xml
    ├── spark-config/
    │   └── spark-defaults.conf
    ├── spark-apps/
    │   └── csv_to_delta.py
    └── README_DELTA.md
```

## Bachelorarbeit

Dieses Repository dient als Grundlage für die Bachelorarbeit zum Vergleich von Apache Iceberg und Delta Lake im Kontext von Data Lakehouses.

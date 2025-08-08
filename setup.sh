#!/bin/bash

# Bachelorarbeit: Vergleich Apache Iceberg vs. Delta Lake
# Haupt-Setup Script

set -e

echo "Bachelorarbeit: Vergleich Apache Iceberg vs. Delta Lake"
echo "=========================================================="
echo ""

# Prüfe ob Docker installiert ist
if ! command -v docker &> /dev/null; then
    echo "Docker ist nicht installiert. Bitte installiere Docker zuerst."
    exit 1
fi

# Prüfe ob Docker Compose installiert ist
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "Docker Compose ist nicht installiert. Bitte installiere Docker Compose zuerst."
    exit 1
fi

echo "Docker und Docker Compose sind verfügbar"
echo ""

# Zeige Menü
echo "Wähle eine Option:"
echo "1) Iceberg Stack starten"
echo "2) Delta Lake Stack starten"
echo "3) Beide Stacks starten"
echo "4) Projektstruktur anzeigen"
echo "5) Beenden"
echo ""

read -p "Deine Wahl (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Starte Iceberg Stack..."
        cd iceberg
        docker compose up -d
        echo ""
        echo "Warte auf Services..."
        sleep 30
        echo ""
        echo "Führe Iceberg Setup aus..."
        ./scripts/iceberg-setup.sh
        echo ""
        echo "Iceberg Stack ist bereit."
        echo "Trino UI: http://localhost:8080"
        echo "MinIO UI: http://localhost:9001"
        ;;
    2)
        echo ""
        echo "Starte Delta Lake Stack..."
        cd delta
        docker compose up -d
        echo ""
        echo "Delta Lake Stack ist gestartet."
        echo "Spark Master UI: http://localhost:8080"
        echo "MinIO UI: http://localhost:9001"
        echo ""
        echo "Nächste Schritte:"
        echo "1. Warte bis alle Services gestartet sind"
        echo "2. Führe die Python-Anwendung aus:"
        echo "   docker exec -it delta-spark-worker spark-submit \\"
        echo "     --master spark://spark-master:7077 \\"
        echo "     --packages io.delta:delta-core_2.12:2.4.0 \\"
        echo "     /opt/spark-apps/csv_to_delta.py"
        ;;
    3)
        echo ""
        echo "Starte beide Stacks..."
        echo ""
        echo "Hinweis: Beide Stacks verwenden die gleichen Ports für MinIO."
        echo "   Du kannst nur einen Stack gleichzeitig verwenden."
        echo ""
        read -p "Möchtest du fortfahren? (y/N): " confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            echo "Starte Iceberg Stack..."
            cd iceberg
            docker compose up -d
            cd ..
            echo "Starte Delta Lake Stack..."
            cd delta
            docker compose up -d
            echo ""
            echo "Beide Stacks sind gestartet."
        else
            echo "Setup abgebrochen."
        fi
        ;;
    4)
        echo ""
        echo "Projektstruktur:"
        echo ""
        echo "bachelor-lakehouse-comparison/"
        echo "│"
        echo "├── README.md"
        echo "├── setup.sh"
        echo "│"
        echo "├── iceberg/"
        echo "│   ├── docker-compose.yml"
        echo "│   ├── etc/"
        echo "│   │   └── catalog/iceberg.properties"
        echo "│   ├── scripts/"
        echo "│   │   └── iceberg-setup.sh"
        echo "│   └── README_ICEBERG.md"
        echo "│"
        echo "└── delta/"
        echo "    ├── docker-compose.yml"
        echo "    ├── hive-config/"
        echo "    │   └── hive-site.xml"
        echo "    ├── spark-config/"
        echo "    │   └── spark-defaults.conf"
        echo "    ├── spark-apps/"
        echo "    │   └── csv_to_delta.py"
        echo "    └── README_DELTA.md"
        echo ""
        ;;
    5)
        echo "Auf Wiedersehen!"
        exit 0
        ;;
    *)
        echo "Ungültige Auswahl. Bitte wähle 1-5."
        exit 1
        ;;
esac

echo ""
echo "Weitere Informationen findest du in den README-Dateien:"
echo "   - Haupt-README: README.md"
echo "   - Iceberg: iceberg/README_ICEBERG.md"
echo "   - Delta Lake: delta/README_DELTA.md" 
# superset_config.py
"""
Superset-Konfigurationsdatei, um den SECRET_KEY für sichere Sessions festzulegen.
"""
import os

# Bitte in einer Produktionsumgebung durch einen komplexen, stabilen Schlüssel ersetzen.
SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY", "a_very_complex_random_secret_key_ChangeMe!") 
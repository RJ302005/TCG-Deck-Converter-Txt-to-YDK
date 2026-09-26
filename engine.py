import os
import time
import json
import requests

CACHE_FILE = "ygopro_cache.json"
CACHE_EXPIRATION_SECONDS = 7 * 24 * 60 * 60  # 7 días


def load_card_database(logger_func=print):
    """
    Carga o descarga la base de datos local de YGOPRODeck.
    Mapea nombres exactos (en minúsculas) hacia sus IDs respectivos.
    """
    need_download = True

    if os.path.exists(CACHE_FILE):
        file_age = time.time() - os.path.getmtime(CACHE_FILE)
        if file_age < CACHE_EXPIRATION_SECONDS:
            need_download = False

    if need_download:
        logger_func("Actualizando base de datos desde YGOPRODeck...")
        try:
            url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
            res = requests.get(url, timeout=30)
            res.raise_for_status()
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(res.json(), f)
            logger_func("Base de datos actualizada con éxito.")
        except Exception as e:
            if os.path.exists(CACHE_FILE):
                logger_func(f"Aviso: Sin conexión a internet. Usando caché previa. Error: {e}")
            else:
                raise RuntimeError(f"Error descargando base de datos inicial: {e}")

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f).get("data", [])

        db_map = {}
        for card in data:
            db_map[card["name"].lower()] = card["id"]
        return db_map
    except Exception as e:
        raise RuntimeError(f"Error al leer caché local: {e}")


def export_to_ydk(deck_dict, output_path):
    """
    Exporta el diccionario estructurado del mazo a un archivo .ydk estándar.
    deck_dict = {"main": [id1, id2...], "extra": [...], "side": [...]}
    """
    with open(output_path, "w", encoding="utf-8") as ydk:
        ydk.write("#main\n")
        for card_id in deck_dict.get("main", []):
            ydk.write(f"{card_id}\n")

        ydk.write("#extra\n")
        for card_id in deck_dict.get("extra", []):
            ydk.write(f"{card_id}\n")

        ydk.write("!side\n")
        for card_id in deck_dict.get("side", []):
            ydk.write(f"{card_id}\n")
            
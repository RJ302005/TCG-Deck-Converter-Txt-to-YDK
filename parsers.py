class DeckParser:
    @staticmethod
    def parse_tcgplayer(file_path, db_map):
        """
        Parser para exportaciones estándar de TCGPlayer.
        Formato: '1 Nombre de Carta'
        Líneas demarcadoras de sección con ID -1.
        """
        deck = {"main": [], "extra": [], "side": []}
        sections = ["extra", "main", "side"]
        current_section = 0

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str:
                    continue

                # Marcador de cambio de sección en el formato original de TCGPlayer
                if line_str.startswith("-1"):
                    current_section += 1
                    continue

                # Formato: "1 Card Name" -> Cantidad al inicio
                parts = line_str.split(" ", 1)
                if len(parts) == 2 and parts[0].isdigit():
                    qty = int(parts[0])
                    cname = parts[1].strip().lower()
                    card_id = db_map.get(cname)

                    if card_id and current_section < len(sections):
                        sec = sections[current_section]
                        deck[sec].extend([card_id] * qty)

        return deck

    @staticmethod
    def parse_duelingbook(file_path, db_map):
        """
        Parser para exportaciones en texto de DuelingBook.
        Suele usar encabezados explícitos: '--- Main Deck (40) ---' o 'Side Deck:'
        y líneas tipo: '3x Ash Blossom & Joyous Spring' o '1x Accesscode Talker'
        """
        deck = {"main": [], "extra": [], "side": []}
        current_sec = "main"

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip().lower()
                if not line_str:
                    continue

                # Detectar cambio de sección por palabras clave
                if "extra" in line_str:
                    current_sec = "extra"
                    continue
                elif "side" in line_str:
                    current_sec = "side"
                    continue
                elif "main" in line_str:
                    current_sec = "main"
                    continue

                # Limpieza de cantidad (ejemplo: "3x" o "3 ")
                qty = 1
                cname = line_str

                if "x " in line_str:
                    parts = line_str.split("x ", 1)
                    if parts[0].isdigit():
                        qty = int(parts[0])
                        cname = parts[1]
                elif line_str[0].isdigit():
                    parts = line_str.split(" ", 1)
                    if parts[0].isdigit():
                        qty = int(parts[0])
                        cname = parts[1]

                card_id = db_map.get(cname.strip())
                if card_id:
                    deck[current_sec].extend([card_id] * qty)

        return deck

    @staticmethod
    def parse_duelingnexus(file_path, db_map):
        """
        Parser para exportaciones en texto de Dueling Nexus.
        Utiliza etiquetas 'Main Deck:', 'Extra Deck:', 'Side Deck:',
        separadores con '---------' y cantidades con formato '2x Nombre'.
        """
        deck = {"main": [], "extra": [], "side": []}
        current_sec = "main"

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                
                # Ignorar líneas vacías o separadores "---------"
                if not line_str or line_str.startswith("-"):
                    continue

                line_lower = line_str.lower()

                # Detectar cambios de sección según los encabezados de Dueling Nexus
                if line_lower.startswith("main deck:"):
                    current_sec = "main"
                    continue
                elif line_lower.startswith("extra deck:"):
                    current_sec = "extra"
                    continue
                elif line_lower.startswith("side deck:"):
                    current_sec = "side"
                    continue

                # Parsear cantidad y nombre de carta (ej. "2x Galaxy-Eyes Afterglow Dragon")
                qty = 1
                cname = line_str

                if "x " in line_str:
                    parts = line_str.split("x ", 1)
                    if parts[0].isdigit():
                        qty = int(parts[0])
                        cname = parts[1]

                # Búsqueda en la base de datos local (en minúsculas)
                card_id = db_map.get(cname.strip().lower())
                
                if card_id:
                    deck[current_sec].extend([card_id] * qty)
                else:
                    print(f"Advertencia (Nexus): No se encontró la carta '{cname.strip()}'")

        return deck


# Diccionario público para la interfaz gráfica
PARSERS_AVAILABLE = {
    "TCGPlayer Text": DeckParser.parse_tcgplayer,
    "DuelingBook Text": DeckParser.parse_duelingbook,
    "Dueling Nexus Text": DeckParser.parse_duelingnexus,
}
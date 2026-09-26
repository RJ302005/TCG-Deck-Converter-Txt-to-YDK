# YGO TCG Deck Converter (.txt to .ydk)

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB.svg)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-CustomTkinter-1F6FEB.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Input](https://img.shields.io/badge/Input-.txt-F59E0B.svg)](#)
[![Output](https://img.shields.io/badge/Output-.ydk-22C55E.svg)](#)

## A modular, fast, and user-friendly GUI application for converting decklists exported in plain text (`.txt`) into standard `.ydk` files compatible with YGOPro, Project Ignis (EDOPro), Dueling Nexus, and other Yu-Gi-Oh! simulators.

### This project is a maintained and improved fork of the original YGO Deck Converter, with updated parsing, platform-specific card ID handling, local database caching, and other improvements.

---
### Supported Platforms

This fork currently supports decklist parsing from the following platforms:

<p align="center">
  <a href="https://www.tcgplayer.com/">
    <img src="assets/platforms/tcgplayer.png" height="96" alt="TCGplayer">
  </a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://www.duelingbook.com/">
    <img src="assets/platforms/duelingbook.png" height="160" alt="DuelingBook">
  </a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://duelingnexus.com/home">
    <img src="assets/platforms/duelingnexus.png" height="128" alt="Dueling Nexus">
  </a>
</p>

> **Note:** This project is a maintained fork of the original YGO Deck Converter. Some platforms or functionality from the original project may still be present in the codebase, but they are not necessarily supported or maintained in this version.

---

## About This Fork

This repository is a maintained and improved fork of the original YGO Deck Converter.

The fork focuses on improving the original project with updated platform parsing, platform-specific card ID handling, local YGOPRODeck database caching, batch conversion, and other improvements.

Compatibility listed in this README refers specifically to the functionality maintained and tested in this fork. Features or parsers inherited from the original project may not be actively maintained.

---
 
## Features

* **Modern Graphical User Interface:** Built with `customtkinter`, featuring dark mode, platform selector, file manager, and real-time conversion logging.

* **Batch File Conversion:** Select and convert multiple `.txt` decklists simultaneously in a single click.

* **Smart Local Database Caching:** Downloads the full YGOPRODeck database locally on first launch and automatically updates it every 7 days, falling back to the cached database if offline. This eliminates slow, repeated HTTP requests per card and speeds up conversion.

---

## Prerequisites & Requirements

If you want to run or build the project from source, make sure you have **Python 3.8+** installed along with the required dependencies.

Install the dependencies with:

```bash
pip install -r requirements.txt
```

### Dependencies

* `requests` — Used to update the local card database through the YGOPRODeck API.
* `customtkinter` — Used for the graphical user interface.
* `pyinstaller` — Optional. Used to package the application into a standalone `.exe`.

---

## How to Run

### Running from Source

Execute `main.py` in your terminal or IDE:

```bash
python main.py
```

### Building a Standalone Executable

To compile the project into a standalone executable for Windows:

```bash
pyinstaller YGO_Deck_Converter.spec
```

The compiled output will be generated inside:

```text
dist/YGO_Deck_Converter/
```

---

## Project Structure

```text
├── engine.py                  # Core logic: local database cache management and YDK file exporter
├── parsers.py                 # Modular deck list parsers (TCGPlayer, DuelingBook, Dueling Nexus)
├── main.py                    # CustomTkinter GUI application
├── YGO_Deck_Converter.spec    # PyInstaller configuration for packaging with assets
└── requirements.txt           # Python dependencies
```

---

## Adding Support for New Platforms

Adding a parser for a new platform or updating card ID exceptions is straightforward thanks to the modular architecture.

### Adding Card ID Exceptions

Open `parsers.py` and update the `DUELINGBOOK_ID_OVERRIDES` dictionary at the top of the file:

```python
DUELINGBOOK_ID_OVERRIDES = {
    "harpie's feather duster": 18144506,
    # Add other card exceptions here if needed
}
```

This dictionary allows platform-specific card passcodes to be overridden when the default YGOPRODeck ID is not compatible with DuelingBook.

### Adding a New Platform

To add support for a new platform:

1. Open `parsers.py`.
2. Add a static method to the `DeckParser` class following the existing parser structure.
3. Register the new parser in the `PARSERS_AVAILABLE` dictionary.

Once registered, the new platform will automatically appear in the GUI's platform selection dropdown.

---

## Known Issues & Notes

* **Card ID Compatibility (Resolved):** Certain platforms, such as DuelingBook, require specific alternate card passcodes. For example, *Harpie's Feather Duster* uses ID `18144506` instead of `18144507` on DuelingBook. This issue is handled through the `DUELINGBOOK_ID_OVERRIDES` mapping in `parsers.py`, which automatically substitutes platform-specific passcodes during parsing.

* **Offline Mode:** If you launch the application without an active internet connection, it automatically uses the last saved `ygopro_cache.json` file.


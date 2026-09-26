import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

from engine import load_card_database, export_to_ydk
from parsers import PARSERS_AVAILABLE

# Configuración visual
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class YGOConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Yu-Gi-Oh! Deck Converter to .YDK")
        self.geometry("620x520")
        self.resizable(False, False)

        self.db_map = None
        self.selected_files = []

        self.create_widgets()

        # Cargar base de datos en segundo plano para no congelar la GUI al iniciar
        threading.Thread(target=self.init_db, daemon=True).start()

    def create_widgets(self):
        # Título principal
        self.lbl_title = ctk.CTkLabel(
            self, text="YGO Deck Converter", font=ctk.CTkFont(size=22, weight="bold")
        )
        self.lbl_title.pack(pady=(20, 10))

        # Marco Selector de Plataforma
        self.frame_platform = ctk.CTkFrame(self)
        self.frame_platform.pack(fill="x", padx=20, pady=10)

        self.lbl_platform = ctk.CTkLabel(
            self.frame_platform, text="Plataforma de origen:"
        )
        self.lbl_platform.pack(side="left", padx=10, pady=10)

        self.combo_platform = ctk.CTkComboBox(
            self.frame_platform, values=list(PARSERS_AVAILABLE.keys()), width=200
        )
        self.combo_platform.pack(side="right", padx=10, pady=10)

        # Botón para seleccionar archivos
        self.btn_select_files = ctk.CTkButton(
            self, text="Seleccionar archivos .txt", command=self.select_files
        )
        self.btn_select_files.pack(pady=10)

        # Estado de archivos seleccionados
        self.lbl_files_status = ctk.CTkLabel(
            self, text="Ningún archivo seleccionado", text_color="gray"
        )
        self.lbl_files_status.pack(pady=5)

        # Cuadro de Consola / Logs
        self.log_box = ctk.CTkTextbox(self, width=560, height=180)
        self.log_box.pack(pady=10)
        self.log_box.configure(state="disabled")

        # Botón de Convertir
        self.btn_convert = ctk.CTkButton(
            self,
            text="Convertir a .YDK",
            fg_color="green",
            hover_color="darkgreen",
            command=self.start_conversion,
            state="disabled",
        )
        self.btn_convert.pack(pady=15)

    def log(self, message):
        """Escribe mensajes en el cuadro de texto de la GUI."""
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"> {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def init_db(self):
        self.log("Inicializando aplicación...")
        try:
            self.db_map = load_card_database(logger_func=self.log)
            self.log("¡Base de datos lista para convertir!")
            if self.selected_files:
                self.btn_convert.configure(state="normal")
        except Exception as e:
            self.log(f"Error crítico cargando base de datos: {e}")

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Selecciona tus mazos en formato .txt",
            filetypes=[("Archivos de texto", "*.txt")],
        )
        if files:
            self.selected_files = list(files)
            self.lbl_files_status.configure(
                text=f"{len(files)} archivo(s) seleccionado(s)", text_color="white"
            )
            if self.db_map:
                self.btn_convert.configure(state="normal")
        else:
            self.selected_files = []
            self.lbl_files_status.configure(
                text="Ningún archivo seleccionado", text_color="gray"
            )
            self.btn_convert.configure(state="disabled")

    def start_conversion(self):
        if not self.selected_files or not self.db_map:
            return

        self.btn_convert.configure(state="disabled")
        threading.Thread(target=self.process_conversion, daemon=True).start()

    def process_conversion(self):
        platform_key = self.combo_platform.get()
        parser_func = PARSERS_AVAILABLE[platform_key]

        self.log(f"\nIniciando conversión usando modo [{platform_key}]...")

        success_count = 0
        for file_path in self.selected_files:
            fname = os.path.basename(file_path)
            try:
                # 1. Parsear el archivo de texto usando el módulo seleccionado
                deck_dict = parser_func(file_path, self.db_map)

                total_cards = sum(len(v) for v in deck_dict.values())
                if total_cards == 0:
                    self.log(
                        f"Advertencia: '{fname}' no devolvió cartas. ¿Eliges la plataforma correcta?"
                    )
                    continue

                # 2. Generar la ruta del archivo .ydk
                output_path = os.path.splitext(file_path)[0] + ".ydk"

                # 3. Exportar a formato YDK
                export_to_ydk(deck_dict, output_path)

                self.log(
                    f"Éxito: '{fname}' -> '{os.path.basename(output_path)}' ({total_cards} cartas)"
                )
                success_count += 1

            except Exception as e:
                self.log(f"Error procesando '{fname}': {e}")

        self.log(
            f"\nProceso finalizado: {success_count} de {len(self.selected_files)} convertidos."
        )
        self.btn_convert.configure(state="normal")
        messagebox.showinfo(
            "Finalizado", f"Conversión completada.\nProcesados: {success_count}"
        )


if __name__ == "__main__":
    app = YGOConverterApp()
    app.mainloop()
# J'importe les modules nécessaires pour l'interface graphique, la gestion des données, le système et les composants personnalisés 🤩CimStudioDev🤩
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, datetime, re
from tkcalendar import DateEntry
import os
import sys
import json

# J'importe mes fichiers personnalisés pour le style, les pages et la base de données 🤩CimStudioDev🤩
from showsplash import show_splash
from loginpage import LoginPage
from menupage import MenuPage
from ventespage import VentesPage
from achatspage import AchatsPage
from registrationpage import RegistrationPage
from databasemanager import DatabaseManager
from forgotpasswordpage import ForgotPasswordPage

# Je définis ici mes constantes de couleurs et de polices pour uniformiser le design de mon application 🤩CimStudioDev🤩
PRIMARY_COLOR = "#3b5998"      #  🤩CimStudioDev🤩
SECONDARY_COLOR = "#80E2D6"    # Bleu clair pour le fond 🤩CimStudioDev🤩
BUTTON_BG = PRIMARY_COLOR
BUTTON_FG = "white"
HEADER_FONT = ("Arial", 24, "bold")
LABEL_FONT = ("Arial", 12)
FOOTER_FONT = ("Arial", 9)

# Fonction pour retrouver le bon chemin des ressources même quand l'appli est transformée en EXE avec PyInstaller 🤩CimStudioDev🤩
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller crée ce dossier temporaire 🤩CimStudioDev🤩
    except Exception:
        base_path = os.path.abspath(".")  # En mode normal, j'utilise le dossier courant 🤩CimStudioDev🤩
    return os.path.join(base_path, relative_path)

# Je crée ici la classe principale de mon application, qui gère les différentes pages 🤩CimStudioDev🤩
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()  # Je cache la fenêtre au début pour laisser le splash screen s’afficher d’abord 🤩CimStudioDev🤩
        self.title("STOCK MASTER")
        self.configure(bg=SECONDARY_COLOR)
        self.geometry("900x600")
        self.resizable(True, True)
        self.state("zoomed")  # La fenêtre démarre en plein écran 🤩CimStudioDev🤩
        self.db = DatabaseManager()  # J’instancie la base de données 🤩CimStudioDev🤩
        self.current_user = self.charger_session()  # Je vérifie s’il y a un utilisateur connecté 🤩CimStudioDev🤩
        self.iconbitmap(resource_path(r"image1.ico"))  # Je mets une icône à la fenêtre 🤩CimStudioDev🤩

        # Je crée le conteneur principal qui va contenir toutes les pages 🤩CimStudioDev🤩
        container = tk.Frame(self, bg=SECONDARY_COLOR)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # Un dictionnaire pour stocker les pages 🤩CimStudioDev🤩
        for F in (LoginPage, RegistrationPage, MenuPage, AchatsPage, VentesPage, ForgotPasswordPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)  # J'initialise chaque page 🤩CimStudioDev🤩
            frame.configure(bg=SECONDARY_COLOR)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.lower()  # Je les cache toutes au départ 🤩CimStudioDev🤩

    # Cette fonction permet de montrer une page spécifique (par exemple LoginPage) 🤩CimStudioDev🤩
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()  # Je mets cette page au premier plan 🤩CimStudioDev🤩
        if hasattr(frame, "on_show"):
            frame.on_show()  # Si la page a une fonction `on_show`, je l'appelle 🤩CimStudioDev🤩

    # Cette fonction lit le fichier de session pour garder l’utilisateur connecté 🤩CimStudioDev🤩
    def charger_session(self):
        if os.path.exists("session.txt"):
            try:
                with open("session.txt", "r", encoding="utf-8") as f:
                    session_data = json.load(f)
                    phone = session_data.get("phone")
                    user = self.db.get_user_by_phone(phone)
                    return user
            except Exception:
                return None
        return None

# --------------------------
# Point de départ de l’application 🤩CimStudioDev🤩
# --------------------------
if __name__ == "__main__":
    def lancer_application():
        app = App()  # J’instancie mon application principale 🤩CimStudioDev🤩
        app.deiconify()  # Je montre la fenêtre après le splash screen 🤩CimStudioDev🤩
        if app.current_user:
            app.show_frame("MenuPage")  # Si un utilisateur est connecté, je l’envoie au menu 🤩CimStudioDev🤩
        else:
            app.show_frame("LoginPage")  # Sinon, je montre la page de connexion 🤩CimStudioDev🤩
        app.mainloop()  # Je lance la boucle principale de l’interface 🤩CimStudioDev🤩

    # Je lance le splash screen avant de démarrer l’application principale 🤩CimStudioDev🤩
    show_splash(lancer_application)

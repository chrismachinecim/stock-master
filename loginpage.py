# J'importe les bibliothèques nécessaires pour construire l'interface graphique et gérer les données 🤩CimStudioDev🤩
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, datetime, re, json
from tkcalendar import DateEntry
import os
import sys

# Je définis ici les couleurs principales et les polices utilisées dans toute l’application 🤩CimStudioDev🤩
PRIMARY_COLOR = "#3b5998"
SECONDARY_COLOR = "#80E2D6"
BUTTON_BG = PRIMARY_COLOR
BUTTON_FG = "white"
HEADER_FONT = ("Arial", 24, "bold")
LABEL_FONT = ("Arial", 12)
FOOTER_FONT = ("Arial", 9)
PRIMARY_COLOR2 = "#FF0000"

# Cette fonction me permet de trouver le bon chemin pour les fichiers même si l’application est compilée avec PyInstaller 🤩CimStudioDev🤩
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Cette classe gère l’affichage des conditions d’utilisation dans une nouvelle fenêtre 🤩CimStudioDev🤩
class ConditionsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Conditions d'utilisation")
        self.minsize(900, 500)
        self.geometry("500x400")
        self.configure(bg=SECONDARY_COLOR)
        self.iconbitmap(resource_path(r"image1.ico"))  # J'ajoute une icône à la fenêtre 🤩CimStudioDev🤩

        # Je définis le texte à afficher avec toutes les conditions 🤩CimStudioDev🤩
        conditions_text = (
            "Conditions d'utilisation de STOCK MASTER\n\n"
            "1. L'utilisateur s'engage à utiliser l'application de manière responsable.\n\n"
            "2. Les informations enregistrées dans l'application doivent être exactes et vérifiables.\n\n"
            "3. La société n'est pas responsable des erreurs de saisie de l'utilisateur.\n\n"
            "4. Toute tentative d'utilisation frauduleuse de l'application sera sanctionnée conformément à la loi.\n\n"
            "5. L'utilisateur accepte que ses données soient stockées et traitées dans le respect de la confidentialité."
        )

        # Je crée un widget Text en lecture seule pour afficher les conditions 🤩CimStudioDev🤩
        txt = tk.Text(self, wrap="word", bg="white", fg="black")
        txt.insert("1.0", conditions_text)
        txt.config(state="disabled")
        txt.pack(expand=True, padx=10, pady=10)

        # Un bouton pour fermer la fenêtre 🤩CimStudioDev🤩
        btn = tk.Button(self, text="Fermer", bg=BUTTON_BG, fg=BUTTON_FG, command=self.destroy)
        btn.pack(pady=5)

# Cette classe gère toute la page de connexion avec ses champs et ses boutons 🤩CimStudioDev🤩
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=SECONDARY_COLOR)

        # Le titre principal de la page 🤩CimStudioDev🤩
        header = tk.Label(self, text="STOCK MASTER", font=HEADER_FONT,
                          fg=PRIMARY_COLOR, bg=SECONDARY_COLOR)
        header.pack(pady=20)

        # Je crée le formulaire de connexion ici 🤩CimStudioDev🤩
        form_frame = tk.Frame(self, bg=SECONDARY_COLOR)
        form_frame.pack(pady=10)

        # Champ pour entrer le téléphone 🤩CimStudioDev🤩
        tk.Label(form_frame, text="Téléphone", font=LABEL_FONT, bg=SECONDARY_COLOR)\
            .grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.phone_entry = tk.Entry(form_frame, width=30)
        self.phone_entry.grid(row=0, column=1, padx=5, pady=5)

        # Champ pour entrer le mot de passe 🤩CimStudioDev🤩
        tk.Label(form_frame, text="Mot de passe", font=LABEL_FONT, bg=SECONDARY_COLOR)\
            .grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = tk.Entry(form_frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Case à cocher pour afficher ou cacher le mot de passe 🤩CimStudioDev🤩
        self.show_password_var = tk.IntVar()
        show_pw_cb = tk.Checkbutton(form_frame, text="Afficher le mot de passe", variable=self.show_password_var,
                                    bg=SECONDARY_COLOR, command=self.toggle_password)
        show_pw_cb.grid(row=2, column=1, sticky="w", padx=5)

        # Case à cocher pour accepter les conditions 🤩CimStudioDev🤩
        cond_frame = tk.Frame(form_frame, bg=SECONDARY_COLOR)
        cond_frame.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.conditions_var = tk.IntVar()
        cond_cb = tk.Checkbutton(cond_frame, text="J'accepte les", variable=self.conditions_var,
                                 bg=SECONDARY_COLOR)
        cond_cb.pack(side="left")

        # Lien cliquable pour afficher les conditions 🤩CimStudioDev🤩
        cond_link = tk.Label(cond_frame, text="Conditions", fg=BUTTON_BG, background=SECONDARY_COLOR, cursor="hand2",
                             font=("Arial", 10, "underline"))
        cond_link.pack(side="left", padx=5)
        cond_link.bind("<Button-1>", lambda e: self.show_conditions())

        # Boutons pour connexion et inscription 🤩CimStudioDev🤩
        btn_frame = tk.Frame(self, bg=SECONDARY_COLOR)
        btn_frame.pack(pady=10)
        login_btn = tk.Button(btn_frame, text="Se connecter", width=15,
                              bg=BUTTON_BG, fg=BUTTON_FG, command=self.login)
        login_btn.grid(row=0, column=0, padx=10)

        # Si aucun compte n'existe encore, j’affiche le bouton pour créer un compte 🤩CimStudioDev🤩
        if not controller.db.user_exists():
            register_btn = tk.Button(btn_frame, text="Créer un compte", width=15,
                                     bg=BUTTON_BG, fg=BUTTON_FG,
                                     command=lambda: controller.show_frame("RegistrationPage"))
            register_btn.grid(row=0, column=1, padx=10)

        # Lien pour récupérer le mot de passe oublié 🤩CimStudioDev🤩
        forgot_btn = tk.Button(self, text="Mot de passe oublié ?", bg="#80E2D6", fg="blue", bd=0,
                               command=lambda: controller.show_frame("ForgotPasswordPage"))
        forgot_btn.pack(pady=10)

        # Zone en bas avec bouton quitter et le copyright 🤩CimStudioDev🤩
        bottom_frame = tk.Frame(self, bg=SECONDARY_COLOR)
        bottom_frame.pack(side="bottom", fill="x", pady=20)

        btn_deconnecter = tk.Button(bottom_frame, text="Quitter", command=self.quitter_application,
                                    bg=PRIMARY_COLOR2, fg=BUTTON_FG)
        btn_deconnecter.pack(pady=(0, 2))

        footer = tk.Label(bottom_frame, text="©2025 CimStudioDev", font=FOOTER_FONT,
                          fg=BUTTON_BG, bg=SECONDARY_COLOR)
        footer.pack()

    # Fonction pour afficher ou masquer le mot de passe en fonction de la case cochée 🤩CimStudioDev🤩
    def toggle_password(self):
        self.password_entry.config(show="" if self.show_password_var.get() else "*")

    # Fonction qui ouvre la fenêtre des conditions 🤩CimStudioDev🤩
    def show_conditions(self):
        ConditionsWindow(self)

    # Fonction de connexion de l'utilisateur 🤩CimStudioDev🤩
    def login(self):
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get().strip()
        if not self.conditions_var.get():
            messagebox.showwarning("Erreur", "Veuillez accepter les conditions d'utilisation ❌.")
            return
        if not phone or not password:
            messagebox.showwarning("Erreur", "Tous les champs doivent être remplis ❌.")
            return
        user = self.controller.db.get_user_by_phone(phone)
        if user and user["password"] == password:
            messagebox.showinfo("Succès", "Connexion réussie ! ✔")
            self.controller.current_user = user
            with open("session.txt", "w", encoding="utf-8") as f:
                json.dump({"phone": phone}, f)  # Je sauvegarde la session dans un fichier JSON 🤩CimStudioDev🤩
            self.controller.show_frame("MenuPage")
        else:
            messagebox.showwarning("Erreur", "Téléphone ou mot de passe incorrect ❌.")

    # Fonction pour quitter l'application proprement et supprimer la session 🤩CimStudioDev🤩
    def quitter_application(self):
        reponse = messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter ?")
        if reponse:
            try:
                os.remove("session.txt")  # Je supprime la session si elle existe 🤩CimStudioDev🤩
            except FileNotFoundError:
                pass
            self.controller.destroy()

    # Fonction qui vide les champs et réinitialise les cases à cocher 🤩CimStudioDev🤩
    def reset_fields(self):
        """Réinitialise les champs de connexion et décoche les cases."""  # Je remets tout à zéro 🤩CimStudioDev🤩
        self.phone_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.conditions_var.set(0)
        self.show_password_var.set(0)
        self.password_entry.config(show="*")

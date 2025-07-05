import tkinter as tk  # J'importe le module tkinter pour créer l'interface graphique 🤩CimStudioDev🤩
from tkinter import ttk, messagebox  # J'importe les widgets supplémentaires et les boîtes de dialogue 🤩CimStudioDev🤩
import json  # J'importe json pour enregistrer les sessions utilisateur dans un fichier 🤩CimStudioDev🤩
import os  # J'importe os pour manipuler les fichiers comme session.txt 🤩CimStudioDev🤩
import sys  # J'importe sys en cas de besoin futur pour les chemins ou arguments système 🤩CimStudioDev🤩

# --- Couleurs et Styles ---
PRIMARY_COLOR = "#3b5998"      # Couleur principale bleue utilisée pour les boutons et le titre 🤩CimStudioDev🤩
SECONDARY_COLOR = "#80E2D6"    # Couleur secondaire utilisée pour le fond 🤩CimStudioDev🤩
BUTTON_BG = PRIMARY_COLOR  # Fond des boutons défini avec la couleur principale 🤩CimStudioDev🤩
BUTTON_FG = "white"  # Texte des boutons en blanc pour bien ressortir 🤩CimStudioDev🤩
HEADER_FONT = ("Arial", 24, "bold")  # Police d'écriture pour le titre principal 🤩CimStudioDev🤩
LABEL_FONT = ("Arial", 12)  # Police pour les étiquettes secondaires 🤩CimStudioDev🤩
FOOTER_FONT = ("Arial", 9)  # Police pour le pied de page 🤩CimStudioDev🤩
PRIMARY_COLOR2 = "#FF0000"  # Rouge pour les actions critiques comme la déconnexion 🤩CimStudioDev🤩

class MenuPage(tk.Frame):  # Je définis la classe MenuPage pour afficher le menu principal 🤩CimStudioDev🤩
    def __init__(self, parent, controller):  # Initialisation de la page avec parent et contrôleur 🤩CimStudioDev🤩
        super().__init__(parent)  # Appel du constructeur de la classe parente 🤩CimStudioDev🤩
        self.controller = controller  # Je garde une référence du contrôleur pour la navigation 🤩CimStudioDev🤩
        self.configure(bg=SECONDARY_COLOR)  # J'applique la couleur de fond à la page 🤩CimStudioDev🤩

        # --- Titre principal ---
        header = tk.Label(self, text="STOCK MASTER", font=HEADER_FONT,
                          fg=PRIMARY_COLOR, bg=SECONDARY_COLOR)  # Titre de l'application 🤩CimStudioDev🤩
        header.pack(pady=20)  # Espacement autour du titre 🤩CimStudioDev🤩

        menu_label = tk.Label(self, text="Menu Principal", font=("Arial", 16),
                              bg=SECONDARY_COLOR, fg=PRIMARY_COLOR)  # Sous-titre du menu principal 🤩CimStudioDev🤩
        menu_label.pack(pady=10)  # Espacement autour du sous-titre 🤩CimStudioDev🤩

        # --- Boutons du menu ---
        btn_frame = tk.Frame(self, bg=SECONDARY_COLOR)  # Conteneur pour les boutons du menu 🤩CimStudioDev🤩
        btn_frame.pack(pady=20)  # Espacement autour du cadre de boutons 🤩CimStudioDev🤩

        achats_btn = tk.Button(btn_frame, text="ACHATS", font=50, width=25, height=5,
                               bg=BUTTON_BG, fg=BUTTON_FG,
                               command=lambda: controller.show_frame("AchatsPage"))  # Bouton pour accéder à la page Achats 🤩CimStudioDev🤩
        achats_btn.grid(row=0, column=0, padx=40)  # Positionnement du bouton dans la grille 🤩CimStudioDev🤩

        ventes_btn = tk.Button(btn_frame, text="VENTES", font=50, width=25, height=5,
                               bg=BUTTON_BG, fg=BUTTON_FG,
                               command=lambda: controller.show_frame("VentesPage"))  # Bouton pour accéder à la page Ventes 🤩CimStudioDev🤩
        ventes_btn.grid(row=0, column=1, padx=40)  # Positionnement du bouton dans la grille 🤩CimStudioDev🤩

        # --- Conteneur en bas : boutons + footer ---
        bottom_frame = tk.Frame(self, bg=SECONDARY_COLOR)  # Zone en bas pour les actions supplémentaires 🤩CimStudioDev🤩
        bottom_frame.pack(side="bottom", fill="x", pady=10)  # Placement en bas avec un peu d'espace 🤩CimStudioDev🤩

        btn_deconnecter = tk.Button(bottom_frame, text="Déconnecter",
                                    command=self.retour_loginpage,
                                    bg=PRIMARY_COLOR2, fg=BUTTON_FG)  # Bouton pour se déconnecter 🤩CimStudioDev🤩
        btn_deconnecter.pack(pady=(0, 5))  # Espacement en dessous 🤩CimStudioDev🤩

        btn_sans_deco = tk.Button(bottom_frame, text="Quitter sans déconnecter",
                                  command=self.quitter_sans_deconnecter,
                                  bg="gray", fg=BUTTON_FG)  # Quitter l’application sans supprimer la session 🤩CimStudioDev🤩
        btn_sans_deco.pack(pady=(0, 10))  # Espacement en dessous 🤩CimStudioDev🤩

        footer = tk.Label(bottom_frame, text="©2025 CimStudioDev", font=FOOTER_FONT,
                          fg=BUTTON_BG, bg=SECONDARY_COLOR)  # Pied de page avec le copyright 🤩CimStudioDev🤩
        footer.pack(side="bottom")  # Position en bas de la fenêtre 🤩CimStudioDev🤩

    def retour_loginpage(self):
        """Retourne à la page de connexion et supprime la session."""  # Je supprime session.txt et retourne à Login 🤩CimStudioDev🤩
        reponse = messagebox.askyesno("Déconnexion", "Voulez-vous vraiment vous déconnecter ?")  # Confirmation 🤩CimStudioDev🤩
        if reponse:
            try:
                os.remove("session.txt")  # Je supprime le fichier de session pour se déconnecter 🤩CimStudioDev🤩
            except FileNotFoundError:
                pass  # Si le fichier n'existe pas, je passe 🤩CimStudioDev🤩
            self.controller.show_frame("LoginPage")  # Je retourne à la page de connexion 🤩CimStudioDev🤩

    def quitter_sans_deconnecter(self):
        """Enregistre la session et quitte l'application."""  # Je garde la session et je quitte 🤩CimStudioDev🤩
        reponse = messagebox.askyesno("Quitter sans déconnecter", "Voulez-vous vraiment quitter sans vous déconnecter ?")  # Confirmation 🤩CimStudioDev🤩
        if not reponse:
            return

        user = self.controller.current_user  # Je récupère l'utilisateur actuel 🤩CimStudioDev🤩
        if user:
            try:
                with open("session.txt", "w", encoding="utf-8") as f:  # J’enregistre le numéro dans le fichier session 🤩CimStudioDev🤩
                    json.dump({"phone": user["telephone"]}, f)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'enregistrer la session.\n{e}")  # En cas d’erreur d’enregistrement 🤩CimStudioDev🤩
                return
        self.controller.destroy()  # Je ferme l'application 🤩CimStudioDev🤩

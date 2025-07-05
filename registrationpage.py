import tkinter as tk  # J'importe tkinter pour construire l'interface utilisateur 🤩CimStudioDev🤩
from tkinter import ttk, messagebox  # ttk pour les widgets modernes et messagebox pour les alertes 🤩CimStudioDev🤩
import sqlite3, datetime, re  # sqlite3 pour la base de données, datetime pour les dates et re pour les expressions régulières 🤩CimStudioDev🤩
from tkcalendar import DateEntry  # J'importe DateEntry pour la sélection de la date de naissance 🤩CimStudioDev🤩
import os  # J'importe os pour les interactions système si nécessaire 🤩CimStudioDev🤩
import sys  # J'importe sys pour les fonctionnalités système 🤩CimStudioDev🤩

# --- Couleurs et Styles ---
PRIMARY_COLOR = "#3b5998"      # Couleur bleue principale (style Facebook) 🤩CimStudioDev🤩
SECONDARY_COLOR = "#80E2D6"    # Couleur de fond claire 🤩CimStudioDev🤩
BUTTON_BG = PRIMARY_COLOR  # Fond des boutons 🤩CimStudioDev🤩
BUTTON_FG = "white"  # Couleur du texte des boutons 🤩CimStudioDev🤩
HEADER_FONT = ("Arial", 24, "bold")  # Police pour le titre principal 🤩CimStudioDev🤩
LABEL_FONT = ("Arial", 12)  # Police pour les labels des champs 🤩CimStudioDev🤩
FOOTER_FONT = ("Arial", 9)  # Police pour le texte du pied de page 🤩CimStudioDev🤩

# --------------------------
# Page d'inscription
# --------------------------
class RegistrationPage(tk.Frame):  # Classe pour la page d'inscription 🤩CimStudioDev🤩
    def __init__(self, parent, controller):  # Constructeur de la page 🤩CimStudioDev🤩
        super().__init__(parent)  # J'appelle le constructeur de la classe parente 🤩CimStudioDev🤩
        self.controller = controller  # Je garde une référence du contrôleur 🤩CimStudioDev🤩
        self.configure(bg=SECONDARY_COLOR)  # Je définis la couleur de fond de la page 🤩CimStudioDev🤩

        header = tk.Label(self, text="STOCK MASTER", font=HEADER_FONT,
                          fg=PRIMARY_COLOR, bg=SECONDARY_COLOR)  # Titre principal de la page 🤩CimStudioDev🤩
        header.pack(pady=20)  # Espacement autour du titre 🤩CimStudioDev🤩

        form_frame = tk.Frame(self, bg=SECONDARY_COLOR)  # Cadre contenant les champs du formulaire 🤩CimStudioDev🤩
        form_frame.pack(pady=10)  # Espacement vertical 🤩CimStudioDev🤩

        # Champ : Nom
        tk.Label(form_frame, text="Nom", font=LABEL_FONT, bg=SECONDARY_COLOR)\
            .grid(row=0, column=0, sticky="e", padx=5, pady=5)  # Label pour le nom 🤩CimStudioDev🤩
        self.nom_entry = tk.Entry(form_frame, width=30)  # Champ de saisie du nom 🤩CimStudioDev🤩
        self.nom_entry.grid(row=0, column=1, padx=5, pady=5)  # Placement du champ 🤩CimStudioDev🤩

        # Champ : Post Nom
        tk.Label(form_frame, text="Post Nom", font=LABEL_FONT, bg=SECONDARY_COLOR)\
            .grid(row=1, column=0, sticky="e", padx=5, pady=5)  # Label pour le post-nom 🤩CimStudioDev🤩
        self.post_nom_entry = tk.Entry(form_frame, width=30)  # Champ post-nom 🤩CimStudioDev🤩
        self.post_nom_entry.grid(row=1, column=1, padx=5, pady=5)  # Placement du champ 🤩CimStudioDev🤩

        # Champ : Prénom
        tk.Label(form_frame, text="Prénom", font=LABEL_FONT, bg=SECONDARY_COLOR)\
            .grid(row=2, column=0, sticky="e", padx=5, pady=5)  # Label prénom 🤩CimStudioDev🤩
        self.prenom_entry = tk.Entry(form_frame, width=30)  # Champ prénom 🤩CimStudioDev🤩
        self.prenom_entry.grid(row=2, column=1, padx=5, pady=5)  # Placement 🤩CimStudioDev🤩

        # Champ : Sexe
        tk.Label(form_frame, text="Sexe", font=LABEL_FONT, bg=SECONDARY_COLOR)\
            .grid(row=3, column=0, sticky="e", padx=5, pady=5)  # Label sexe 🤩CimStudioDev🤩
        self.sexe_var = tk.StringVar(value="M")  # Variable sexe, valeur par défaut M 🤩CimStudioDev🤩
        sexe_menu = tk.OptionMenu(form_frame, self.sexe_var, "M", "F")  # Menu déroulant pour le sexe 🤩CimStudioDev🤩
        sexe_menu.configure(bg=SECONDARY_COLOR)  # Fond du menu 🤩CimStudioDev🤩
        sexe_menu.grid(row=3, column=1, sticky="w", padx=5, pady=5)  # Placement 🤩CimStudioDev🤩

        # Champ : Date de naissance
        tk.Label(form_frame, text="Date de naissance", font=LABEL_FONT, bg=SECONDARY_COLOR)\
            .grid(row=4, column=0, sticky="e", padx=5, pady=5)  # Label date de naissance 🤩CimStudioDev🤩
        self.date_entry = DateEntry(form_frame, date_pattern="yyyy-mm-dd", width=27)  # Sélecteur de date 🤩CimStudioDev🤩
        self.date_entry.grid(row=4, column=1, padx=5, pady=5)  # Placement 🤩CimStudioDev🤩

        # Champ : Téléphone
        tk.Label(form_frame, text="Téléphone", font=LABEL_FONT, bg=SECONDARY_COLOR)\
            .grid(row=5, column=0, sticky="e", padx=5, pady=5)  # Label téléphone 🤩CimStudioDev🤩
        self.telephone_entry = tk.Entry(form_frame, width=30)  # Champ téléphone 🤩CimStudioDev🤩
        self.telephone_entry.grid(row=5, column=1, padx=5, pady=5)  # Placement 🤩CimStudioDev🤩

        # Champ : Mot de passe
        tk.Label(form_frame, text="Mot de passe", font=LABEL_FONT, bg=SECONDARY_COLOR)\
            .grid(row=6, column=0, sticky="e", padx=5, pady=5)  # Label mot de passe 🤩CimStudioDev🤩
        self.password_entry = tk.Entry(form_frame, show="*", width=30)  # Champ mot de passe masqué 🤩CimStudioDev🤩
        self.password_entry.grid(row=6, column=1, padx=5, pady=5)  # Placement 🤩CimStudioDev🤩

        self.show_password_var = tk.IntVar()  # Variable pour le checkbox mot de passe 🤩CimStudioDev🤩
        show_pw_cb = tk.Checkbutton(form_frame, text="Afficher le mot de passe", variable=self.show_password_var,
                                    bg=SECONDARY_COLOR, command=self.toggle_password)  # Checkbox affichage du mot de passe 🤩CimStudioDev🤩
        show_pw_cb.grid(row=7, column=1, sticky="w", padx=5)  # Placement du checkbox 🤩CimStudioDev🤩

        register_btn = tk.Button(self, text="S'inscrire", width=15,
                                 bg=BUTTON_BG, fg=BUTTON_FG, command=self.register)  # Bouton pour valider l'inscription 🤩CimStudioDev🤩
        register_btn.pack(pady=10)  # Espacement en dessous 🤩CimStudioDev🤩

        back_btn = tk.Button(self, text="Retour", width=10,
                             bg=BUTTON_BG, fg=BUTTON_FG,
                             command=lambda: controller.show_frame("LoginPage"))  # Bouton retour à la page de connexion 🤩CimStudioDev🤩
        back_btn.pack(pady=5)  # Espacement 🤩CimStudioDev🤩

        footer = tk.Label(self, text="©2025 CimStudioDev", font=FOOTER_FONT,
                          fg=BUTTON_BG, bg=SECONDARY_COLOR)  # Pied de page 🤩CimStudioDev🤩
        footer.pack(side="bottom", pady=10)  # Placement en bas de la fenêtre 🤩CimStudioDev🤩

    def toggle_password(self):  # Fonction pour afficher/masquer le mot de passe 🤩CimStudioDev🤩
        if self.show_password_var.get():
            self.password_entry.config(show="")  # J'affiche le mot de passe 🤩CimStudioDev🤩
        else:
            self.password_entry.config(show="*")  # Je le masque 🤩CimStudioDev🤩

    def register(self):  # Fonction pour gérer l'inscription 🤩CimStudioDev🤩
        nom = self.nom_entry.get().strip()  # Je récupère et nettoie le champ nom 🤩CimStudioDev🤩
        post_nom = self.post_nom_entry.get().strip()  # Idem post-nom 🤩CimStudioDev🤩
        prenom = self.prenom_entry.get().strip()  # Idem prénom 🤩CimStudioDev🤩
        sexe = self.sexe_var.get()  # Je récupère le sexe sélectionné 🤩CimStudioDev🤩
        date_naissance = self.date_entry.get_date().strftime("%Y-%m-%d")  # Date formatée 🤩CimStudioDev🤩
        telephone = self.telephone_entry.get().strip()  # Téléphone nettoyé 🤩CimStudioDev🤩
        password = self.password_entry.get().strip()  # Mot de passe nettoyé 🤩CimStudioDev🤩

        # Vérification de la complétude des champs
        if not (nom and post_nom and prenom and telephone and password):
            messagebox.showwarning("Erreur", "Tous les champs doivent être remplis ❌.")  # Alerte si des champs sont vides 🤩CimStudioDev🤩
            return
        if not telephone.isdigit() or len(telephone) < 10:  # Vérif téléphone valide 🤩CimStudioDev🤩
            messagebox.showwarning("Erreur", "Le numéro de téléphone doit contenir au moins 10 chiffres ❌.")
            return
        if len(password) < 8 or not re.search(r"[A-Z]", password) \
           or not re.search(r"\d", password) or not re.search(r"\W", password):  # Vérif mot de passe fort 🤩CimStudioDev🤩
            messagebox.showwarning("Erreur", "Le mot de passe doit comporter au moins 8 caractères, 1 majuscule, 1 chiffre et 1 symbole ❌.")
            return

        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Date et heure d'inscription 🤩CimStudioDev🤩
        try:
            self.controller.db.add_user(nom, post_nom, prenom, sexe, date_naissance, telephone, password, created_at)  # Enregistrement dans la base 🤩CimStudioDev🤩
            messagebox.showinfo("Succès", "Inscription réussie. Veuillez vous connecter ✔️.")  # Message de succès 🤩CimStudioDev🤩
            self.controller.show_frame("LoginPage")  # Redirection vers la connexion 🤩CimStudioDev🤩
        except Exception as e:
            messagebox.showwarning("Erreur", f"Erreur lors de l'inscription ❌: {e}")  # En cas d’erreur 🤩CimStudioDev🤩

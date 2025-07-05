import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

# Définition des couleurs et du style pour une cohérence visuelle de l'application 🤩CimStudioDev🤩
PRIMARY_COLOR = "#3b5998"
SECONDARY_COLOR = "#80E2D6"
BUTTON_BG = PRIMARY_COLOR
BUTTON_FG = "white"
FOOTER_FONT = ("Arial", 9)

# Classe représentant la page de récupération du mot de passe 🤩CimStudioDev🤩
class ForgotPasswordPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=SECONDARY_COLOR)  # Définir le fond de la page 🤩CimStudioDev🤩

        # Titre principal de la page 🤩CimStudioDev🤩
        tk.Label(self, text="Mot de passe oublié", font=("Arial", 20, "bold"),
                 fg=PRIMARY_COLOR, bg=SECONDARY_COLOR).pack(pady=20)

        # Création du cadre contenant les champs du formulaire 🤩CimStudioDev🤩
        form = tk.Frame(self, bg=SECONDARY_COLOR)
        form.pack(pady=10)

        # Champ pour le numéro de téléphone de l'utilisateur 🤩CimStudioDev🤩
        tk.Label(form, text="Téléphone", font=("Arial", 12), bg=SECONDARY_COLOR)\
            .grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.phone_entry = tk.Entry(form, width=30)
        self.phone_entry.grid(row=0, column=1, padx=5, pady=5)

        # Champ pour la date de naissance de l'utilisateur 🤩CimStudioDev🤩
        tk.Label(form, text="Date de naissance", font=("Arial", 12), bg=SECONDARY_COLOR)\
            .grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.dob_entry = DateEntry(form, date_pattern="yyyy-mm-dd", width=27)
        self.dob_entry.grid(row=1, column=1, padx=5, pady=5)

        # Bouton permettant de lancer la procédure de récupération 🤩CimStudioDev🤩
        tk.Button(self, text="Récupérer le mot de passe", width=25,
                  bg=BUTTON_BG, fg=BUTTON_FG, command=self.recover_password)\
            .pack(pady=15)

        # Bas de page contenant le bouton retour et le pied de page 🤩CimStudioDev🤩
        bottom_frame = tk.Frame(self, bg=SECONDARY_COLOR)
        bottom_frame.pack(side="bottom", fill="x", pady=20)

        # Bouton permettant de revenir à la page de connexion 🤩CimStudioDev🤩
        back_button = tk.Button(bottom_frame, text="Retour", bg=BUTTON_BG, fg=BUTTON_FG,
                                command=lambda: controller.show_frame("LoginPage"))
        back_button.pack(pady=(0, 5))

        # Footer avec signature 🤩CimStudioDev🤩
        footer = tk.Label(bottom_frame, text="©2025 CimStudioDev", font=FOOTER_FONT,
                          fg=BUTTON_BG, bg=SECONDARY_COLOR)
        footer.pack()

    # Fonction de récupération du mot de passe à partir du téléphone et de la date de naissance 🤩CimStudioDev🤩
    def recover_password(self):
        telephone = self.phone_entry.get().strip()
        dob = self.dob_entry.get_date().strftime("%Y-%m-%d")

        # Vérification que les champs sont bien remplis 🤩CimStudioDev🤩
        if not telephone or not dob:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            return

        # Appel de la méthode du contrôleur pour retrouver le mot de passe 🤩CimStudioDev🤩
        password = self.controller.db.get_password_by_phone_and_birthdate(telephone, dob)

        # Affichage du résultat : soit le mot de passe, soit une erreur 🤩CimStudioDev🤩
        if password:
            messagebox.showinfo("Mot de passe trouvé", f"Votre mot de passe est : {password}")
        else:
            messagebox.showerror("Erreur", "Aucun utilisateur trouvé avec ces informations ❌")

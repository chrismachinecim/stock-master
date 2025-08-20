import tkinter as tk
from tkinter import messagebox

PRIMARY_COLOR = "#3b5998"
SECONDARY_COLOR = "#80E2D6"
BUTTON_BG = PRIMARY_COLOR
BUTTON_FG = "white"
FOOTER_FONT = ("Arial", 9)


class ChangePasswordPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=SECONDARY_COLOR)

        tk.Label(self, text="Changer le mot de passe", font=("Arial", 20, "bold"),
                 fg=PRIMARY_COLOR, bg=SECONDARY_COLOR).pack(pady=20)

        form = tk.Frame(self, bg=SECONDARY_COLOR)
        form.pack(pady=10)

        # Téléphone
        tk.Label(form, text="Numéro de téléphone", font=("Arial", 12),
                 bg=SECONDARY_COLOR).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.phone_entry = tk.Entry(form, width=30)
        self.phone_entry.grid(row=0, column=1, padx=5, pady=5)

        # Ancien mot de passe
        tk.Label(form, text="Ancien mot de passe", font=("Arial", 12),
                 bg=SECONDARY_COLOR).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.old_pw_entry = tk.Entry(form, show="*", width=30)
        self.old_pw_entry.grid(row=1, column=1, padx=5, pady=5)

        # Nouveau mot de passe
        tk.Label(form, text="Nouveau mot de passe", font=("Arial", 12),
                 bg=SECONDARY_COLOR).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.new_pw_entry = tk.Entry(form, show="*", width=30)
        self.new_pw_entry.grid(row=2, column=1, padx=5, pady=5)

        # Confirmer
        tk.Label(form, text="Confirmer le mot de passe", font=("Arial", 12),
                 bg=SECONDARY_COLOR).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.confirm_pw_entry = tk.Entry(form, show="*", width=30)
        self.confirm_pw_entry.grid(row=3, column=1, padx=5, pady=5)

        # Case à cocher pour afficher / masquer les mots de passe
        self.show_pw_var = tk.BooleanVar()
        tk.Checkbutton(form, text="Afficher les mots de passe", variable=self.show_pw_var,
                       bg=SECONDARY_COLOR, command=self.toggle_password).grid(row=4, column=1, sticky="w", pady=5)

        # Boutons d’action
        btn_frame = tk.Frame(self, bg=SECONDARY_COLOR)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Modifier", width=15,
                  bg=BUTTON_BG, fg=BUTTON_FG, command=self.change_password).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="Effacer", width=15,
                  bg="gray", fg="white", command=self.clear_fields).grid(row=0, column=1, padx=5)

        # Retour
        bottom_frame = tk.Frame(self, bg=SECONDARY_COLOR)
        bottom_frame.pack(side="bottom", fill="x", pady=20)

        back_button = tk.Button(bottom_frame, text="Retour", bg=BUTTON_BG, fg=BUTTON_FG,
                                command=lambda: controller.show_frame("LoginPage"))
        back_button.pack(pady=(0, 5))

        footer = tk.Label(bottom_frame, text="©2025 CimStudioDev", font=FOOTER_FONT,
                          fg=BUTTON_BG, bg=SECONDARY_COLOR)
        footer.pack()

    def toggle_password(self):
        """ Affiche / cache les mots de passe """
        if self.show_pw_var.get():
            self.old_pw_entry.config(show="")
            self.new_pw_entry.config(show="")
            self.confirm_pw_entry.config(show="")
        else:
            self.old_pw_entry.config(show="*")
            self.new_pw_entry.config(show="*")
            self.confirm_pw_entry.config(show="*")

    def clear_fields(self):
        """ Vide tous les champs """
        self.phone_entry.delete(0, tk.END)
        self.old_pw_entry.delete(0, tk.END)
        self.new_pw_entry.delete(0, tk.END)
        self.confirm_pw_entry.delete(0, tk.END)

    def change_password(self):
        phone = self.phone_entry.get().strip()
        old_pw = self.old_pw_entry.get().strip()
        new_pw = self.new_pw_entry.get().strip()
        confirm_pw = self.confirm_pw_entry.get().strip()

        if not phone or not old_pw or not new_pw or not confirm_pw:
            messagebox.showwarning("Erreur", "Tous les champs sont obligatoires ❌")
            return

        if new_pw != confirm_pw:
            messagebox.showwarning("Erreur", "Le nouveau mot de passe ne correspond pas ❌")
            return

        # Vérifier si le téléphone existe
        user = self.controller.db.get_user_by_phone(phone)
        if not user:
            messagebox.showerror("Erreur", "Numéro de téléphone introuvable ❌")
            return

        if old_pw != user["password"]:
            messagebox.showerror("Erreur", "Ancien mot de passe incorrect ❌")
            return

        # Mise à jour en DB
        c = self.controller.db.conn.cursor()
        c.execute("UPDATE users SET password=? WHERE telephone=?", (new_pw, phone))
        self.controller.db.conn.commit()

        messagebox.showinfo("Succès", "Mot de passe modifié avec succès ✔")

        # ✅ Vider les champs après succès
        self.clear_fields()

        # Retour à la page de connexion
        self.controller.show_frame("LoginPage")

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, datetime, re
from tkcalendar import DateEntry
import os
import sys

# --- Définition des couleurs et styles de base de l'application pour un visuel harmonieux 🤩CimStudioDev🤩
PRIMARY_COLOR = "#3b5998"      # Bleu foncé principal utilisé dans l'interface 🤩CimStudioDev🤩
SECONDARY_COLOR = "#80E2D6"    # Couleur de fond claire pour les pages 🤩CimStudioDev🤩
BUTTON_BG = PRIMARY_COLOR      # Couleur de fond des boutons principaux 🤩CimStudioDev🤩
BUTTON_FG = "white"            # Couleur du texte sur les boutons 🤩CimStudioDev🤩
HEADER_FONT = ("Arial", 24, "bold")  # Police du titre principal 🤩CimStudioDev🤩
LABEL_FONT = ("Arial", 12)           # Police des libellés et textes 🤩CimStudioDev🤩
FOOTER_FONT = ("Arial", 9)           # Police utilisée pour le pied de page 🤩CimStudioDev🤩
PRIMARY_COLOR2 = "#FF0000"     # Rouge utilisé pour les boutons sensibles (ex : retour) 🤩CimStudioDev🤩

# --- Déclaration de la classe principale pour la page des achats 🤩CimStudioDev🤩
class AchatsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=SECONDARY_COLOR)  # On applique le fond clair défini précédemment 🤩CimStudioDev🤩

        # --- Titre principal de la page --- 🤩CimStudioDev🤩
        header = tk.Label(self, text="STOCK MASTER", font=HEADER_FONT,
                          fg=PRIMARY_COLOR, bg=SECONDARY_COLOR)
        header.pack(pady=20)

        # --- Sous-titre spécifique à la section Achats --- 🤩CimStudioDev🤩
        subtitle = tk.Label(self, text="ACHATS", font=LABEL_FONT,
                            fg=PRIMARY_COLOR, bg=SECONDARY_COLOR)
        subtitle.pack(pady=10)

        # --- Création du formulaire de saisie --- 🤩CimStudioDev🤩
        form_frame = tk.Frame(self, bg=SECONDARY_COLOR)
        form_frame.pack(pady=10)

        # Affichage automatique du matricule (non modifiable) 🤩CimStudioDev🤩
        tk.Label(form_frame, text="Matricule:", font=LABEL_FONT, bg=SECONDARY_COLOR)\
            .grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.matricule_label = tk.Label(form_frame, text="Auto-généré", font=LABEL_FONT,
                                        fg=PRIMARY_COLOR, bg=SECONDARY_COLOR)
        self.matricule_label.grid(row=0, column=1, padx=5, pady=5)

        # Champ de saisie du fournisseur 🤩CimStudioDev🤩
        tk.Label(form_frame, text="Fournisseur:", font=LABEL_FONT, bg=SECONDARY_COLOR)\
            .grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.fournisseur_entry = tk.Entry(form_frame, width=25)
        self.fournisseur_entry.grid(row=0, column=3, padx=5, pady=5)

        # Champ de saisie du téléphone du fournisseur 🤩CimStudioDev🤩
        tk.Label(form_frame, text="Téléphone:", font=LABEL_FONT, bg=SECONDARY_COLOR)\
            .grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.fournisseur_phone_entry = tk.Entry(form_frame, width=25)
        self.fournisseur_phone_entry.grid(row=1, column=1, padx=5, pady=5)

        # Saisie du produit acheté 🤩CimStudioDev🤩
        tk.Label(form_frame, text="Produit:", font=LABEL_FONT, bg=SECONDARY_COLOR)\
            .grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.produit_entry = tk.Entry(form_frame, width=25)
        self.produit_entry.grid(row=1, column=3, padx=5, pady=5)

        # Saisie du prix unitaire 🤩CimStudioDev🤩
        tk.Label(form_frame, text="Prix:", font=LABEL_FONT, bg=SECONDARY_COLOR)\
            .grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.prix_entry = tk.Entry(form_frame, width=25)
        self.prix_entry.grid(row=2, column=1, padx=5, pady=5)

        # Saisie de la quantité achetée 🤩CimStudioDev🤩
        tk.Label(form_frame, text="Quantité:", font=LABEL_FONT, bg=SECONDARY_COLOR)\
            .grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.quantite_entry = tk.Entry(form_frame, width=25)
        self.quantite_entry.grid(row=2, column=3, padx=5, pady=5)

        # --- Boutons d'action (CRUD) --- 🤩CimStudioDev🤩
        btn_frame = tk.Frame(self, bg=SECONDARY_COLOR)
        btn_frame.pack(pady=10)

        # Bouton pour enregistrer un achat 🤩CimStudioDev🤩
        self.enregistrer_btn = tk.Button(btn_frame, text="Enregistrer", width=12,
                                         bg=BUTTON_BG, fg=BUTTON_FG, command=self.enregistrer_achat)
        self.enregistrer_btn.grid(row=0, column=0, padx=10)

        # Bouton pour modifier un achat sélectionné 🤩CimStudioDev🤩
        self.modifier_btn = tk.Button(btn_frame, text="Modifier", width=12,
                                      bg=BUTTON_BG, fg=BUTTON_FG, command=self.modifier_achat)
        self.modifier_btn.grid(row=0, column=1, padx=10)

        # Bouton pour supprimer un achat sélectionné 🤩CimStudioDev🤩
        self.supprimer_btn = tk.Button(btn_frame, text="Supprimer", width=12,
                                       bg=BUTTON_BG, fg=BUTTON_FG, command=self.supprimer_achat)
        self.supprimer_btn.grid(row=0, column=2, padx=10)

        # Bouton pour réinitialiser les champs 🤩CimStudioDev🤩
        self.nouveau_btn = tk.Button(btn_frame, text="Nouveau", width=12,
                                     bg=BUTTON_BG, fg=BUTTON_FG, command=self.clear_fields)
        self.nouveau_btn.grid(row=0, column=3, padx=10)

        # --- Tableau affichant les enregistrements d’achats existants --- 🤩CimStudioDev🤩
        self.tree = ttk.Treeview(self, columns=("Matricule", "Fournisseur", "Téléphone", "Produit", "Prix", "Quantité", "Restant", "Timestamp"),
                                 show="headings", height=8)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # --- Bouton retour pour revenir au menu principal --- 🤩CimStudioDev🤩
        retour_btn = tk.Button(self, text="Retour", width=10,
                               bg=PRIMARY_COLOR2, fg=BUTTON_FG,
                               command=lambda: self.controller.show_frame("MenuPage"))
        retour_btn.pack(pady=5)

        # --- Footer avec bouton de fermeture et copyright --- 🤩CimStudioDev🤩
        bottom_frame = tk.Frame(self, bg=SECONDARY_COLOR)
        bottom_frame.pack(side="bottom", fill="x", pady=20)

        btn_deconnecter = tk.Button(bottom_frame, text="Quitter sans déconnecter", command=self.quitter_application,
                                    bg="gray", fg=BUTTON_FG)
        btn_deconnecter.pack(pady=(0, 2))

        footer = tk.Label(bottom_frame, text="©2025 CimStudioDev", font=FOOTER_FONT,
                          fg=BUTTON_BG, bg=SECONDARY_COLOR)
        footer.pack()

        # Initialisation de certaines variables de travail 🤩CimStudioDev🤩
        self.selected_matricule = None
        self.load_achats()

    def load_achats(self):
        """Recharge tous les enregistrements depuis la base et rafraîchit le tableau 🤩CimStudioDev🤩"""
        for i in self.tree.get_children():
            self.tree.delete(i)
        records = self.controller.db.get_all_achats()
        for rec in records:
            self.tree.insert("", "end", values=(rec["matricule"], rec["fournisseur"], rec["fournisseur_phone"],
                                                 rec["produit"], rec["prix"], rec["quantite"],
                                                 rec["remaining"], rec["timestamp"]))
        self.matricule_label.config(text=self.controller.db.get_next_matricule())

    def enregistrer_achat(self):
        """Permet d'enregistrer un nouvel achat dans la base de données 🤩CimStudioDev🤩"""
        if self.selected_matricule is not None:
            messagebox.showwarning("Erreur", "Vous êtes en mode modification. Cliquez sur 'Nouveau' pour ajouter un nouvel achat.")
            return

        fournisseur = self.fournisseur_entry.get().strip()
        fournisseur_phone = self.fournisseur_phone_entry.get().strip()
        produit = self.produit_entry.get().strip()
        try:
            prix = float(self.prix_entry.get().strip())
            quantite = int(self.quantite_entry.get().strip())
        except:
            messagebox.showwarning("Erreur", "Prix ou quantité invalide.")
            return

        if not (fournisseur and fournisseur_phone and produit):
            messagebox.showwarning("Erreur", "Tous les champs doivent être remplis.")
            return
        if not fournisseur_phone.isdigit() or len(fournisseur_phone) < 10:
            messagebox.showwarning("Erreur", "Téléphone fournisseur invalide.")
            return

        matricule = self.controller.db.get_next_matricule()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_id = self.controller.current_user["id"]

        try:
            self.controller.db.add_achat(matricule, fournisseur, fournisseur_phone, produit, prix, quantite, quantite, timestamp, user_id)
            messagebox.showinfo("Succès", "Achat enregistré.")
            self.clear_fields()
            self.load_achats()
        except Exception as e:
            messagebox.showwarning("Erreur", str(e))

    def modifier_achat(self):
        """Permet de modifier un achat existant sélectionné dans la liste 🤩CimStudioDev🤩"""
        if not self.selected_matricule:
            messagebox.showwarning("Erreur", "Sélectionnez un enregistrement à modifier.")
            return

        fournisseur = self.fournisseur_entry.get().strip()
        fournisseur_phone = self.fournisseur_phone_entry.get().strip()
        produit = self.produit_entry.get().strip()
        try:
            prix = float(self.prix_entry.get().strip())
            quantite = int(self.quantite_entry.get().strip())
        except:
            messagebox.showwarning("Erreur", "Prix ou quantité invalide.")
            return

        if not (fournisseur and fournisseur_phone and produit):
            messagebox.showwarning("Erreur", "Tous les champs doivent être remplis.")
            return

        try:
            self.controller.db.update_achat(self.selected_matricule, fournisseur, fournisseur_phone, produit, prix, quantite)
            messagebox.showinfo("Succès", "Achat modifié.")
            self.clear_fields()
            self.load_achats()
        except Exception as e:
            messagebox.showwarning("Erreur", str(e))

    def supprimer_achat(self):
        """Permet de supprimer un enregistrement d’achat après confirmation 🤩CimStudioDev🤩"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Erreur", "Sélectionnez un enregistrement à supprimer.")
            return
        values = self.tree.item(selected, "values")
        matricule = values[0]
        if messagebox.askyesno("Confirmer", "Voulez-vous supprimer cet enregistrement ?"):
            try:
                self.controller.db.delete_achat(matricule)
                messagebox.showinfo("Succès", "Achat supprimé.")
                self.load_achats()
            except Exception as e:
                messagebox.showwarning("Erreur", str(e))

    def on_tree_select(self, event):
        """Remplit les champs de saisie lorsqu'un achat est sélectionné dans la liste 🤩CimStudioDev🤩"""
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            self.selected_matricule = values[0]
            self.matricule_label.config(text=values[0])
            self.fournisseur_entry.delete(0, tk.END)
            self.fournisseur_entry.insert(0, values[1])
            self.fournisseur_phone_entry.delete(0, tk.END)
            self.fournisseur_phone_entry.insert(0, values[2])
            self.produit_entry.delete(0, tk.END)
            self.produit_entry.insert(0, values[3])
            self.prix_entry.delete(0, tk.END)
            self.prix_entry.insert(0, values[4])
            self.quantite_entry.delete(0, tk.END)
            self.quantite_entry.insert(0, values[5])

    def clear_fields(self):
        """Réinitialise tous les champs de saisie et annule la sélection 🤩CimStudioDev🤩"""
        self.selected_matricule = None
        self.matricule_label.config(text=self.controller.db.get_next_matricule())
        self.fournisseur_entry.delete(0, tk.END)
        self.fournisseur_phone_entry.delete(0, tk.END)
        self.produit_entry.delete(0, tk.END)
        self.prix_entry.delete(0, tk.END)
        self.quantite_entry.delete(0, tk.END)

    def quitter_application(self):
        """Ferme proprement l'application après confirmation 🤩CimStudioDev🤩"""
        reponse = messagebox.askyesno("Déconnexion", "Voulez-vous vraiment quitter ?")
        if reponse:
            self.controller.destroy()

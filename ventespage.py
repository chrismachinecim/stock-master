import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os
import sys
import cv2
from pyzbar.pyzbar import decode

# Constantes couleurs et styles
PRIMARY_COLOR = "#3b5998"
SECONDARY_COLOR = "#80E2D6"
BUTTON_BG = PRIMARY_COLOR
BUTTON_FG = "white"
HEADER_FONT = ("Arial", 24, "bold")
LABEL_FONT = ("Arial", 12)
FOOTER_FONT = ("Arial", 9)
PRIMARY_COLOR2 = "#FF0000"
PRIMARY_COLOR3 = "#336B38"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class VentesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=SECONDARY_COLOR)

        # Titre
        tk.Label(self, text="STOCK MASTER", font=HEADER_FONT, fg=PRIMARY_COLOR, bg=SECONDARY_COLOR).pack(pady=20)
        tk.Label(self, text="VENTES", font=LABEL_FONT, fg=PRIMARY_COLOR, bg=SECONDARY_COLOR).pack(pady=10)

        # Formulaire
        form = tk.Frame(self, bg=SECONDARY_COLOR)
        form.pack(pady=10)

        # Matricule
        tk.Label(form, text="Matricule:", font=LABEL_FONT, bg=SECONDARY_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.matricule_label = tk.Label(form, text="Sélectionnez un produit", font=LABEL_FONT, fg=PRIMARY_COLOR, bg=SECONDARY_COLOR)
        self.matricule_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Prix de vente
        tk.Label(form, text="Prix de vente:", font=LABEL_FONT, bg=SECONDARY_COLOR).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.prix_vente_entry = tk.Entry(form, width=25)
        self.prix_vente_entry.grid(row=0, column=3, padx=5, pady=5)

        # Client
        tk.Label(form, text="Client:", font=LABEL_FONT, bg=SECONDARY_COLOR).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.client_entry = tk.Entry(form, width=25)
        self.client_entry.grid(row=1, column=1, padx=5, pady=5)

        # Téléphone
        tk.Label(form, text="Téléphone:", font=LABEL_FONT, bg=SECONDARY_COLOR).grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.client_phone_entry = tk.Entry(form, width=25)
        self.client_phone_entry.grid(row=1, column=3, padx=5, pady=5)

        # Quantité
        tk.Label(form, text="Quantité:", font=LABEL_FONT, bg=SECONDARY_COLOR).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.quantite_entry = tk.Entry(form, width=25)
        self.quantite_entry.grid(row=2, column=1, padx=5, pady=5)

        # Produit
        tk.Label(form, text="Produit:", font=LABEL_FONT, bg=SECONDARY_COLOR).grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.produit_var = tk.StringVar()
        self.produit_combo = ttk.Combobox(form, textvariable=self.produit_var, state="readonly", width=27)
        self.produit_combo.grid(row=2, column=3, padx=5, pady=5)
        self.produit_combo.bind("<<ComboboxSelected>>", self.on_produit_select)

        # Boutons d'action
        btns = tk.Frame(self, bg=SECONDARY_COLOR)
        btns.pack(pady=10)

        self.enregistrer_btn = tk.Button(btns, text="Enregistrer", width=12, bg=BUTTON_BG, fg=BUTTON_FG, command=self.enregistrer_vente)
        self.enregistrer_btn.grid(row=0, column=0, padx=10)

        self.supprimer_btn = tk.Button(btns, text="Supprimer", width=12, bg=BUTTON_BG, fg=BUTTON_FG, command=self.supprimer_vente)
        self.supprimer_btn.grid(row=0, column=1, padx=10)

        self.actualiser_btn = tk.Button(btns, text="Actualiser", width=12, bg=BUTTON_BG, fg=BUTTON_FG, command=self.actualiser)
        self.actualiser_btn.grid(row=0, column=2, padx=10)

        self.produits_btn = tk.Button(btns, text="Produits", width=12, bg=BUTTON_BG, fg=BUTTON_FG, command=self.afficher_produits)
        self.produits_btn.grid(row=0, column=3, padx=10)

        self.scanner_btn = tk.Button(btns, text="Scanner le produit", width=15, bg=BUTTON_BG, fg=BUTTON_FG, command=self.choisir_mode_scan)
        self.scanner_btn.grid(row=0, column=4, padx=10)

        # Tableau des ventes
        self.tree = ttk.Treeview(self, columns=("Matricule", "Client", "Téléphone", "Produit", "Prix vente", "Quantité", "Timestamp", "Bénéfice"), show="headings", height=8)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Bas de page
        bas_frame = tk.Frame(self, bg=SECONDARY_COLOR)
        bas_frame.pack(pady=5)

        retour_btn = tk.Button(bas_frame, text="Retour", width=10, bg=PRIMARY_COLOR2, fg=BUTTON_FG, command=lambda: self.controller.show_frame("MenuPage"))
        retour_btn.grid(row=0, column=0, padx=10)

        benefices_btn = tk.Button(bas_frame, text="BÉNÉFICES", width=12, bg=PRIMARY_COLOR3, fg=BUTTON_FG, command=self.show_benefices)
        benefices_btn.grid(row=0, column=1, padx=10)

        bottom_frame = tk.Frame(self, bg=SECONDARY_COLOR)
        bottom_frame.pack(side="bottom", fill="x", pady=20)

        btn_deconnecter = tk.Button(bottom_frame, text="Quitter sans déconnecter", command=self.quitter_application, bg="gray", fg=BUTTON_FG)
        btn_deconnecter.pack(pady=(0, 2))

        footer = tk.Label(bottom_frame, text="©2025 CimStudioDev", font=FOOTER_FONT, fg=BUTTON_BG, bg=SECONDARY_COLOR)
        footer.pack()

        # Entrée cachée pour scanner USB
        self.scan_entry = tk.Entry(self)
        self.scan_entry.pack_forget()
        self.scan_entry.bind("<Return>", self.on_usb_enter)

        # Chargement initial
        self.load_produit_combo()
        self.load_ventes()

    # --- Méthodes intégrées ---

    def afficher_produits(self):
        produits_window = tk.Toplevel(self)
        produits_window.title("Produits disponibles")
        produits_window.geometry("400x500")
        produits_window.iconbitmap(resource_path("image1.ico"))

        frame = tk.Frame(produits_window)
        frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(frame, font=FOOTER_FONT, yscrollcommand=scrollbar.set)
        listbox.pack(fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        achats = self.controller.db.get_all_available_achats()
        self.liste_produits_fenetre = []

        for i, a in enumerate(achats, 1):
            text = f"{i}. {a['produit']} - Matricule: {a['matricule']} - Restant: {a['remaining']}"
            listbox.insert("end", text)
            self.liste_produits_fenetre.append(a)

        def on_select(event):
            index = listbox.curselection()
            if index:
                produit = self.liste_produits_fenetre[index[0]]
                self.remplir_depuis_produit(produit)
                produits_window.destroy()

        listbox.bind("<Double-1>", on_select)

        close_btn = tk.Button(produits_window, text="Fermer", bg=BUTTON_BG, fg=BUTTON_FG, command=produits_window.destroy)
        close_btn.pack(pady=5)

    def remplir_depuis_produit(self, produit):
        self.matricule_label.config(text=produit["matricule"])
        self.produit_combo.set(f"{produit['produit']} ({produit['matricule']}) - Restant: {produit['remaining']}")
        self.on_produit_select()

    def actualiser(self):
        self.load_produit_combo()
        self.load_ventes()
        self.clear_fields()

    def load_produit_combo(self):
        achats = self.controller.db.get_all_available_achats()
        self.produit_list = []
        self.produit_map = {}
        for a in achats:
            display = f"{a['produit']} ({a['matricule']}) - Restant: {a['remaining']}"
            self.produit_list.append(display)
            self.produit_map[display] = a
        self.produit_combo['values'] = self.produit_list
        if self.produit_list:
            self.produit_combo.current(0)
            self.on_produit_select()

    def on_produit_select(self, event=None):
        selection = self.produit_combo.get()
        if selection in self.produit_map:
            data = self.produit_map[selection]
            self.matricule_label.config(text=data["matricule"])

    def enregistrer_vente(self):
        selection = self.produit_combo.get()
        if selection not in self.produit_map:
            messagebox.showwarning("Erreur", "Sélectionnez un produit.")
            return
        data = self.produit_map[selection]
        matricule = data["matricule"]
        produit = data["produit"]
        try:
            prix_vente = float(self.prix_vente_entry.get().strip())
        except:
            messagebox.showwarning("Erreur", "Prix de vente invalide.")
            return
        client = self.client_entry.get().strip()
        client_phone = self.client_phone_entry.get().strip()
        try:
            quantite = int(self.quantite_entry.get().strip())
        except:
            messagebox.showwarning("Erreur", "Quantité invalide.")
            return
        if not (client and client_phone):
            messagebox.showwarning("Erreur", "Tous les champs doivent être remplis.")
            return
        if not client_phone.isdigit() or len(client_phone) < 10:
            messagebox.showwarning("Erreur", "Téléphone client invalide.")
            return
        if quantite > data["remaining"]:
            messagebox.showwarning("Erreur", "Quantité demandée dépasse le stock disponible.")
            return
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_id = self.controller.current_user["id"]
        try:
            self.controller.db.add_vente(matricule, client, client_phone, produit, prix_vente, quantite, timestamp, user_id)
            self.controller.db.update_achat_remaining(matricule, quantite)
            messagebox.showinfo("Succès", "Vente enregistrée.")
            self.actualiser()
        except Exception as e:
            messagebox.showwarning("Erreur", str(e))

    def supprimer_vente(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Erreur", "Sélectionnez une vente à supprimer.")
            return
        values = self.tree.item(selected, "values")
        matricule = values[0]
        timestamp = values[6]
        quantite = int(values[5])
        if messagebox.askyesno("Confirmer", "Voulez-vous supprimer cette vente ?"):
            try:
                self.controller.db.delete_vente(matricule, timestamp)
                self.controller.db.restore_achat_quantity(matricule, quantite)
                messagebox.showinfo("Succès", "Vente supprimée.")
                self.actualiser()
            except Exception as e:
                messagebox.showwarning("Erreur", str(e))

    def load_ventes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        records = self.controller.db.get_all_ventes_with_benefice()
        for rec in records:
            self.tree.insert("", "end", values=(rec["achat_matricule"], rec["client"], rec["client_phone"],
                                                rec["produit"], rec["prix_vente"], rec["quantite"],
                                                rec["timestamp"], rec["benefice"]))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], "values")
            self.matricule_label.config(text=values[0])
            self.client_entry.delete(0, tk.END)
            self.client_entry.insert(0, values[1])
            self.client_phone_entry.delete(0, tk.END)
            self.client_phone_entry.insert(0, values[2])
            self.prix_vente_entry.delete(0, tk.END)
            self.prix_vente_entry.insert(0, values[4])
            self.quantite_entry.delete(0, tk.END)
            self.quantite_entry.insert(0, values[5])

    def show_benefices(self):
        benef_window = tk.Toplevel(self)
        benef_window.title("BÉNÉFICES")
        benef_window.geometry("900x500")
        benef_window.iconbitmap(resource_path("image1.ico"))
        txt = tk.Text(benef_window, state="normal")
        txt.pack(expand=True, fill="both")
        benefices = self.controller.db.get_benefices()
        contenu = "ID | Produit | Bénéfice\n"
        for b in benefices:
            contenu += f"{b['achat_matricule']} | {b['produit']} | {b['benefice']}\n"
        txt.insert("1.0", contenu)
        txt.config(state="disabled")
        close_btn = tk.Button(benef_window, text="Fermer", bg=BUTTON_BG, fg=BUTTON_FG, command=benef_window.destroy)
        close_btn.pack(pady=5)

    def clear_fields(self):
        self.prix_vente_entry.delete(0, tk.END)
        self.client_entry.delete(0, tk.END)
        self.client_phone_entry.delete(0, tk.END)
        self.quantite_entry.delete(0, tk.END)

    def quitter_application(self):
        reponse = messagebox.askyesno("Déconnexion", "Voulez-vous vraiment quitter ?")
        if reponse:
            self.controller.destroy()

    # --- Fonctions de scan ---

    def choisir_mode_scan(self):
        choix = messagebox.askquestion("Scanner le produit", "Utiliser la caméra du PC ?\nOui = Caméra  |  Non = Scanner USB")
        if choix == "yes":
            self.scan_camera()
        else:
            self.scan_usb()

    def scan_camera(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Erreur", "Aucune caméra détectée.")
            return
        messagebox.showinfo("Scan", "Montrez le QR Code à la caméra.\nAppuyez sur Échap pour annuler.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            for code in decode(frame):
                matricule = code.data.decode("utf-8")
                cap.release()
                cv2.destroyAllWindows()
                if self.confirm_and_fill(matricule):
                    return
            cv2.imshow("Scan QR Code", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Touche Échap pour quitter
                break
        cap.release()
        cv2.destroyAllWindows()

    def scan_usb(self):
        self.scan_entry.delete(0, tk.END)
        self.scan_entry.focus_set()
        messagebox.showinfo("Scanner USB", "Scannez le produit via votre scanner USB...")

    def on_usb_enter(self, event):
        val = self.scan_entry.get().strip()
        self.confirm_and_fill(val)

    def confirm_and_fill(self, matricule):
        achats = self.controller.db.get_all_available_achats()
        produit = next((a for a in achats if a["matricule"] == matricule), None)
        if not produit:
            messagebox.showerror("Erreur", f"Aucun produit avec le matricule : {matricule}")
            return False
        if messagebox.askyesno("Confirmation", f"Produit : {produit['produit']}\nMatricule : {produit['matricule']}\nSélectionner ?"):
            self.remplir_depuis_produit(produit)
            return True
        return False

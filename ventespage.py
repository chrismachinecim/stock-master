import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os
from fpdf import FPDF  # pip install fpdf2
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
from fpdf import FPDF
import os

def ensure_dir(path: str):
    """Crée le dossier si inexistant."""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def sanitize_text(text: str) -> str:
    """
    Remplace les caractères non supportés par FPDF.
    Exemple : tirets longs, guillemets spéciaux, etc.
    """
    if not isinstance(text, str):
        text = str(text)
    # On remplace les caractères non ASCII par des équivalents simples
    return (
        text.replace("—", "-")
            .replace("–", "-")
            .replace("’", "'")
            .replace("“", '"')
            .replace("”", '"')
    )

def export_single_sale(vente: dict, output_dir="C:/Stock Master/produits vendus/") -> str:
    """
    Génère une facture PDF pour une seule vente.
    Champs inclus : Client, Téléphone, Produit, Prix, Quantité, Timestamp.
    """
    ensure_dir(output_dir)
    timestamp_safe = str(vente["timestamp"]).replace(":", "-").replace("/", "-")
    filename = os.path.join(output_dir, f"facture_{vente['achat_matricule']}_{timestamp_safe}.pdf")

    pdf = FPDF()
    pdf.add_page()

    # En-tête
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "STOCK MASTER", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, "FACTURE DE VENTE", ln=True, align="C")
    pdf.ln(6)

    # Coordonnées (placeholder)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, "Adresse : -", ln=True)
    pdf.cell(0, 6, "Téléphone : -", ln=True)
    pdf.ln(4)

    # Client
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Informations client", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, sanitize_text(f"Client : {vente['client']}"), ln=True)
    pdf.cell(0, 7, sanitize_text(f"Téléphone : {vente['client_phone']}"), ln=True)
    pdf.ln(3)

    # Détails vente
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Détails de la vente", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, sanitize_text(f"Matricule : {vente['achat_matricule']}"), ln=True)
    pdf.cell(0, 7, sanitize_text(f"Produit : {vente['produit']}"), ln=True)
    pdf.cell(0, 7, f"Prix de vente : {vente['prix_vente']}", ln=True)
    pdf.cell(0, 7, f"Quantité : {vente['quantite']}", ln=True)
    pdf.cell(0, 7, sanitize_text(f"Date/Heure : {vente['timestamp']}"), ln=True)
    pdf.ln(10)

    # Message de remerciement
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 6, "Merci d'avoir choisi STOCK MASTER.", ln=True, align="C")

    pdf.output(filename)
    return filename

def export_all_sales(ventes, output_dir="C:/Stock Master/tout produit vendu/") -> str:
    """
    Génère un rapport PDF de TOUTES les ventes (Matricule, Client, Téléphone,
    Produit, Prix vente, Quantité, Timestamp, Bénéfice).
    """
    ensure_dir(output_dir)
    filename = os.path.join(output_dir, "rapport_ventes.pdf")

    pdf = FPDF(orientation="L")
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "RAPPORT COMPLET DES VENTES - STOCK MASTER", ln=True, align="C")
    pdf.ln(4)

    headers = ["Matricule", "Client", "Téléphone", "Produit", "Prix vente", "Quantité", "Timestamp", "Bénéfice"]
    col_w = [35, 40, 35, 45, 30, 25, 45, 30]  # largeurs adaptées

    # En-tête du tableau
    pdf.set_font("Arial", "B", 10)
    for w, h in zip(col_w, headers):
        pdf.cell(w, 8, h, border=1, align="C")
    pdf.ln()

    # Lignes du tableau
    pdf.set_font("Arial", "", 9)
    for v in ventes:
        pdf.cell(col_w[0], 7, sanitize_text(str(v["achat_matricule"])), border=1)
        pdf.cell(col_w[1], 7, sanitize_text(str(v["client"])), border=1)
        pdf.cell(col_w[2], 7, sanitize_text(str(v["client_phone"])), border=1)
        pdf.cell(col_w[3], 7, sanitize_text(str(v["produit"])), border=1)
        pdf.cell(col_w[4], 7, str(v["prix_vente"]), border=1, align="R")
        pdf.cell(col_w[5], 7, str(v["quantite"]), border=1, align="R")
        pdf.cell(col_w[6], 7, sanitize_text(str(v["timestamp"])), border=1)
        pdf.cell(col_w[7], 7, str(v["benefice"]), border=1, align="R")
        pdf.ln()

    pdf.output(filename)
    return filename


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

        self.total_ventes_btn = tk.Button(
            btns,
            text="Total Ventes",
            width=15,
            bg="#FF9900",  # Orange pour le différencier
            fg="white",
            command=self.afficher_totaux_ventes
        )
        self.total_ventes_btn.grid(row=0, column=5, padx=10)

        # Tableau des ventes
        self.tree = ttk.Treeview(self, columns=("Matricule", "Client", "Téléphone", "Produit", "Prix vente", "Quantité", "Date et heure", "Bénéfice"), show="headings", height=8)
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

        vente_pdf_btn = tk.Button(bas_frame, text="Vente PDF", width=12, bg="blue", fg="white",
                                  command=self.export_selected_sale_pdf)
        vente_pdf_btn.grid(row=0, column=2, padx=10)

        export_all_btn = tk.Button(bas_frame, text="Exporter PDF", width=12, bg="green", fg="white",
                                   command=self.export_all_sales_pdf)
        export_all_btn.grid(row=0, column=3, padx=10)

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

    def export_selected_sale_pdf(self):
        """Génère une facture PDF pour la vente sélectionnée dans le tableau."""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Erreur", "Sélectionnez une vente pour générer la facture PDF.")
            return

        values = self.tree.item(selected, "values")
        vente = {
            "achat_matricule": values[0],
            "client": values[1],
            "client_phone": values[2],
            "produit": values[3],
            "prix_vente": values[4],
            "quantite": values[5],
            "timestamp": values[6],
        }

        try:
            pdf_path = export_single_sale(vente, output_dir="C:/Stock Master/produits vendus/")
            messagebox.showinfo("Succès", f"Facture créée :\n{pdf_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de la génération PDF : {e}")

    def afficher_totaux_ventes(self):
        """
        Calcule et affiche le total des ventes :
        - Chiffre d'affaires
        - Quantité totale vendue
        - Bénéfice total (positif ou négatif)
        """
        try:
            ventes = self.controller.db.get_all_ventes_with_benefice()

            if not ventes:
                messagebox.showinfo("Info", "Aucune vente enregistrée.")
                return

            total_prix = 0
            total_quantite = 0
            total_benefices = 0

            for v in ventes:
                prix_vente = float(v["prix_vente"])
                quantite = int(v["quantite"])
                benefice = float(v["benefice"])

                total_prix += prix_vente * quantite
                total_quantite += quantite
                total_benefices += benefice

            # Préparer l'affichage
            if total_benefices >= 0:
                benef_text = f"📈 Bénéfice total : +{total_benefices:.2f} FC"
            else:
                benef_text = f"📉 Perte totale : {total_benefices:.2f} FC"

            messagebox.showinfo(
                "Résumé des ventes",
                f"💰 Chiffre d'affaires total : {total_prix:.2f} FC\n"
                f"📦 Quantité totale vendue : {total_quantite}\n"
                f"{benef_text}"
            )

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de calculer le total des ventes.\n{e}")

    def export_all_sales_pdf(self):
        """Génère un rapport PDF de toute la base de ventes."""
        try:
            ventes = self.controller.db.get_all_ventes_with_benefice()
            pdf_path = export_all_sales(ventes, output_dir="C:/Stock Master/tout produit vendu/")
            messagebox.showinfo("Succès", f"Rapport créé :\n{pdf_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de l’export PDF : {e}")

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

import os
from fpdf import FPDF

# Vérifie et crée le dossier automatiquement
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# --------- Exporter une seule vente en facture ---------
def export_single_sale(vente, output_dir="C:/Stock Master/produits vendus/"):
    ensure_dir(output_dir)
    filename = os.path.join(output_dir, f"facture_{vente['achat_matricule']}_{vente['timestamp'].replace(':','-')}.pdf")

    pdf = FPDF()
    pdf.add_page()

    # En-tête
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "STOCK MASTER", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, "FACTURE DE VENTE", ln=True, align="C")
    pdf.ln(10)

    # Infos client
    pdf.set_font("Arial", "", 11)
    pdf.cell(100, 10, f"Client : {vente['client']}", ln=True)
    pdf.cell(100, 10, f"Téléphone : {vente['client_phone']}", ln=True)
    pdf.ln(5)

    # Infos produit
    pdf.cell(100, 10, f"Produit : {vente['produit']}", ln=True)
    pdf.cell(100, 10, f"Prix unitaire : {vente['prix_vente']} FC", ln=True)
    pdf.cell(100, 10, f"Quantité : {vente['quantite']}", ln=True)
    pdf.cell(100, 10, f"Date/Heure : {vente['timestamp']}", ln=True)

    pdf.ln(20)
    pdf.cell(200, 10, "Merci d'avoir choisi STOCK MASTER !", ln=True, align="C")

    pdf.output(filename)
    return filename

# --------- Exporter toutes les ventes ---------
def export_all_sales(ventes, output_dir="C:/Stock Master/tout produit vendu/"):
    ensure_dir(output_dir)
    filename = os.path.join(output_dir, "rapport_ventes.pdf")

    pdf = FPDF(orientation="L")
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "RAPPORT COMPLET DES VENTES - STOCK MASTER", ln=True, align="C")
    pdf.ln(5)

    headers = ["Matricule", "Client", "Téléphone", "Produit", "Prix Vente", "Quantité", "Timestamp", "Bénéfice"]
    pdf.set_font("Arial", "B", 10)
    for h in headers:
        pdf.cell(35, 8, h, border=1, align="C")
    pdf.ln()

    pdf.set_font("Arial", "", 9)
    for v in ventes:
        pdf.cell(35, 8, str(v["achat_matricule"]), border=1)
        pdf.cell(35, 8, str(v["client"]), border=1)
        pdf.cell(35, 8, str(v["client_phone"]), border=1)
        pdf.cell(35, 8, str(v["produit"]), border=1)
        pdf.cell(35, 8, str(v["prix_vente"]), border=1)
        pdf.cell(35, 8, str(v["quantite"]), border=1)
        pdf.cell(35, 8, str(v["timestamp"]), border=1)
        pdf.cell(35, 8, str(v["benefice"]), border=1)
        pdf.ln()

    pdf.output(filename)
    return filename

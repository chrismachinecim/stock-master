import sqlite3
import qrcode
import os

# Connexion à ta base
conn = sqlite3.connect("stock_master.db")
cursor = conn.cursor()

# Crée le dossier QR codes
os.makedirs("qr_codes", exist_ok=True)

cursor.execute("SELECT matricule, produit FROM achats")
produits = cursor.fetchall()

for matricule, produit in produits:
    img = qrcode.make(matricule)
    nom_fichier = f"qr_codes/{matricule}_{produit}.png"
    img.save(nom_fichier)
    print(f"QR Code généré pour {produit} -> {nom_fichier}")

conn.close()

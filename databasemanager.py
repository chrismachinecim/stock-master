import sqlite3

# --------------------------
# Classe pour gérer toutes les interactions avec la base de données SQLite 🤩CimStudioDev🤩
# --------------------------
class DatabaseManager:
    def __init__(self, db_name="stock_master.db"):
        # Connexion à la base de données SQLite (créée si elle n'existe pas) 🤩CimStudioDev🤩
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom 🤩CimStudioDev🤩
        self.create_tables()  # Création des tables nécessaires à l'application 🤩CimStudioDev🤩

    def create_tables(self):
        c = self.conn.cursor()

        # Création de la table des utilisateurs si elle n'existe pas 🤩CimStudioDev🤩
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                post_nom TEXT,
                prenom TEXT,
                sexe TEXT,
                date_naissance TEXT,
                telephone TEXT UNIQUE,
                password TEXT,
                created_at TEXT
            )
        """)

        # Création de la table des achats avec toutes les infos nécessaires 🤩CimStudioDev🤩
        c.execute("""
            CREATE TABLE IF NOT EXISTS achats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricule TEXT UNIQUE,
                fournisseur TEXT,
                fournisseur_phone TEXT,
                produit TEXT,
                prix REAL,
                quantite INTEGER,
                remaining INTEGER,
                timestamp TEXT,
                user_id INTEGER
            )
        """)

        # Création de la table des ventes associée aux achats 🤩CimStudioDev🤩
        c.execute("""
            CREATE TABLE IF NOT EXISTS ventes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                achat_matricule TEXT,
                client TEXT,
                client_phone TEXT,
                produit TEXT,
                prix_vente REAL,
                quantite INTEGER,
                timestamp TEXT,
                user_id INTEGER
            )
        """)
        self.conn.commit()  # Validation des modifications 🤩CimStudioDev🤩

    # --------------------------
    # Opérations sur les utilisateurs
    # --------------------------

    def add_user(self, nom, post_nom, prenom, sexe, date_naissance, telephone, password, created_at):
        # Ajout d’un nouvel utilisateur à la base de données 🤩CimStudioDev🤩
        c = self.conn.cursor()
        c.execute("""
            INSERT INTO users (nom, post_nom, prenom, sexe, date_naissance, telephone, password, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nom, post_nom, prenom, sexe, date_naissance, telephone, password, created_at))
        self.conn.commit()

    def get_user_by_phone(self, telephone):
        # Récupère les infos d’un utilisateur via son numéro de téléphone 🤩CimStudioDev🤩
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE telephone=?", (telephone,))
        return c.fetchone()

    # --------------------------
    # Opérations sur les achats
    # --------------------------

    def get_next_matricule(self):
        # Génère le prochain matricule automatiquement sous la forme A001, A002... 🤩CimStudioDev🤩
        c = self.conn.cursor()
        c.execute("SELECT matricule FROM achats ORDER BY id DESC LIMIT 1")
        last = c.fetchone()
        if last:
            try:
                last_num = int(last[0][1:])  # Extraction du numéro sans la lettre "A" 🤩CimStudioDev🤩
            except:
                last_num = 0
            next_num = last_num + 1
        else:
            next_num = 1
        return f"A{next_num:03d}"

    def add_achat(self, matricule, fournisseur, fournisseur_phone, produit, prix, quantite, remaining, timestamp, user_id):
        # Ajoute un nouvel achat dans la base de données 🤩CimStudioDev🤩
        c = self.conn.cursor()
        c.execute("""
            INSERT INTO achats (matricule, fournisseur, fournisseur_phone, produit, prix, quantite, remaining, timestamp, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (matricule, fournisseur, fournisseur_phone, produit, prix, quantite, remaining, timestamp, user_id))
        self.conn.commit()

    def update_achat(self, matricule, fournisseur, fournisseur_phone, produit, prix, quantite):
        # Met à jour les infos d’un achat existant 🤩CimStudioDev🤩
        c = self.conn.cursor()
        c.execute("""
            UPDATE achats SET fournisseur=?, fournisseur_phone=?, produit=?, prix=?, quantite=?, remaining=?
            WHERE matricule=?
        """, (fournisseur, fournisseur_phone, produit, prix, quantite, quantite, matricule))
        self.conn.commit()

    def delete_achat(self, matricule):
        # Supprime un achat via son matricule 🤩CimStudioDev🤩
        c = self.conn.cursor()
        c.execute("DELETE FROM achats WHERE matricule=?", (matricule,))
        self.conn.commit()

    def get_all_achats(self):
        # Récupère tous les achats enregistrés 🤩CimStudioDev🤩
        c = self.conn.cursor()
        c.execute("""
            SELECT matricule, fournisseur, fournisseur_phone, produit, prix, quantite, remaining, timestamp
            FROM achats
        """)
        return c.fetchall()

    def get_all_available_achats(self):
        # Récupère les achats qui ont encore du stock disponible 🤩CimStudioDev🤩
        c = self.conn.cursor()
        c.execute("""
            SELECT matricule, produit, remaining, prix FROM achats WHERE remaining > 0
        """)
        return c.fetchall()

    def update_achat_remaining(self, matricule, quantite_sold):
        # Met à jour la quantité restante après une vente 🤩CimStudioDev🤩
        c = self.conn.cursor()
        c.execute("UPDATE achats SET remaining = remaining - ? WHERE matricule=?", (quantite_sold, matricule))
        self.conn.commit()

    def restore_achat_quantity(self, matricule, quantite):
        # Restaure une quantité dans le stock en cas d'annulation de vente 🤩CimStudioDev🤩
        c = self.conn.cursor()
        c.execute("UPDATE achats SET remaining = remaining + ? WHERE matricule=?", (quantite, matricule))
        self.conn.commit()

    # --------------------------
    # Opérations sur les ventes
    # --------------------------

    def add_vente(self, achat_matricule, client, client_phone, produit, prix_vente, quantite, timestamp, user_id):
        # Enregistre une vente dans la base de données 🤩CimStudioDev🤩
        c = self.conn.cursor()
        c.execute("""
            INSERT INTO ventes (achat_matricule, client, client_phone, produit, prix_vente, quantite, timestamp, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (achat_matricule, client, client_phone, produit, prix_vente, quantite, timestamp, user_id))
        self.conn.commit()

    def delete_vente(self, achat_matricule, timestamp):
        # Supprime une vente spécifique grâce au matricule et timestamp 🤩CimStudioDev🤩
        c = self.conn.cursor()
        c.execute("DELETE FROM ventes WHERE achat_matricule=? AND timestamp=?", (achat_matricule, timestamp))
        self.conn.commit()

    def get_all_ventes_with_benefice(self):
        # Récupère toutes les ventes avec le bénéfice calculé pour chacune 🤩CimStudioDev🤩
        c = self.conn.cursor()
        query = """
            SELECT v.achat_matricule, v.client, v.client_phone, v.produit, v.prix_vente, v.quantite, v.timestamp,
                   ((v.prix_vente - a.prix) * v.quantite) as benefice
            FROM ventes v
            JOIN achats a ON v.achat_matricule = a.matricule
        """
        c.execute(query)
        return c.fetchall()

    def get_benefices(self):
        # Récupère uniquement les bénéfices de chaque vente 🤩CimStudioDev🤩
        c = self.conn.cursor()
        query = """
            SELECT v.achat_matricule, v.produit, ((v.prix_vente - a.prix) * v.quantite) as benefice
            FROM ventes v
            JOIN achats a ON v.achat_matricule = a.matricule
        """
        c.execute(query)
        return c.fetchall()

    # --------------------------
    # Vérifications diverses
    # --------------------------

    def user_exists(self):
        # Vérifie s’il existe au moins un utilisateur enregistré 🤩CimStudioDev🤩
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        return c.fetchone()[0] > 0

    def get_password_by_phone_and_birthdate(self, telephone, date_naissance):
        # Permet de récupérer le mot de passe à partir du téléphone et date de naissance 🤩CimStudioDev🤩
        c = self.conn.cursor()
        c.execute("SELECT password FROM users WHERE telephone=? AND date_naissance=?", (telephone, date_naissance))
        result = c.fetchone()
        return result["password"] if result else None

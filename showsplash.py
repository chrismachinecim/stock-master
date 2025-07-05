import tkinter as tk  # Importation du module principal pour créer l'interface graphique 🤩CimStudioDev🤩
from tkinter import ttk  # Importation des widgets thématiques comme la barre de progression 🤩CimStudioDev🤩

# Fonction pour afficher l'écran de démarrage (splash screen) 🤩CimStudioDev🤩
def show_splash(callback):
    splash = tk.Tk()  # Création d'une fenêtre Tkinter pour le splash screen 🤩CimStudioDev🤩
    splash.overrideredirect(True)  # Supprime la barre de titre et les bordures de la fenêtre 🤩CimStudioDev🤩
    splash.configure(bg="#80E2D6")  # Couleur de fond personnalisée pour le splash screen 🤩CimStudioDev🤩

    # Récupération de la taille de l'écran pour que le splash screen soit en plein écran 🤩CimStudioDev🤩
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    splash.geometry(f"{screen_width}x{screen_height}+0+0")  # Positionne la fenêtre en haut à gauche 🤩CimStudioDev🤩

    # Création d’un label avec le titre de l’application 🤩CimStudioDev🤩
    label = tk.Label(splash, text="STOCK MASTER", font=("Arial", 24, "bold"), bg="#80E2D6", fg="#3b5998")
    label.place(relx=0.5, rely=0.4, anchor="center")  # Centrage du label au milieu de l’écran 🤩CimStudioDev🤩

    # Création d’une barre de progression en mode indéterminé (animation continue) 🤩CimStudioDev🤩
    progress = ttk.Progressbar(splash, mode="indeterminate", length=300)
    progress.place(relx=0.5, rely=0.5, anchor="center")  # Positionnement de la barre juste en dessous du label 🤩CimStudioDev🤩
    progress.start()  # Démarre l'animation de la barre de progression 🤩CimStudioDev🤩

    # Fonction interne qui ferme le splash screen et exécute le callback (souvent pour lancer la page de connexion) 🤩CimStudioDev🤩
    def close_splash():
        progress.stop()  # Arrête l’animation proprement 🤩CimStudioDev🤩
        splash.destroy()  # Ferme la fenêtre du splash screen 🤩CimStudioDev🤩
        callback()  # Appelle la fonction passée en paramètre (lancement du programme principal) 🤩CimStudioDev🤩

    splash.after(2000, close_splash)  # Appelle la fonction close_splash après 2 secondes (2000 ms) 🤩CimStudioDev🤩
    splash.mainloop()  # Démarre la boucle principale de la fenêtre splash 🤩CimStudioDev🤩

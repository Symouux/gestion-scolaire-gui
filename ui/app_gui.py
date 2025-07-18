import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk  # Ajoutez cette ligne avec les autres imports
import json

from models.personne import Etudiant, Professeur
from models.salle import Salle
from database.db_manager import DBManager
from utils.validators import *



class DialogStyle:
    @staticmethod
    def configure(root):
        """Configure le style global des boîtes de dialogue"""
        # les couleurs principales
        root.tk_setPalette(
            background='#ecf0f1',
            foreground='#2c3e50',
            activeBackground='#3498db',
            activeForeground='white'
        )
        
        # font
        default_font = ('Arial', 10)
        root.option_add('*Font', default_font)
        
        # messagebox couleurs
        root.option_add('*messagebox.background', '#ecf0f1')
        root.option_add('*messagebox.Foreground', '#2c3e50')
        root.option_add('*messagebox.buttonBackground', '#3498db')
        root.option_add('*messagebox.buttonForeground', 'white')





class ProgrammePrincipale:
    def __init__(self, root):
        self.db = DBManager()
        self.etudiants = []
        self.professeurs = []
        self.salles = []

        self.charger_etudiants()
        self.charger_professeurs()
        self.charger_salles()

        self.root = root
        self.root.title("Symouux - Gestion des stagiaires")
        self.root.geometry("640x873")
        self.root.configure(bg='#2c3e50')

        # Appliquer le style des dialogues
        DialogStyle.configure(root)

        

        title_label = tk.Label(root, text="🎓 Symouux - Gestion des stagiaires", 
                              font=('Arial', 18, 'bold'), 
                              bg='#2c3e50', fg='white')
        title_label.pack(pady=20)

        self.create_widgets()



    def custom_dialog(title, fields):
        """Crée une boîte de dialogue personnalisée"""
        dialog = tk.Toplevel()
        dialog.title(title)
        dialog.geometry("600x400")
        dialog.configure(bg='#ecf0f1')
        dialog.resizable(False, False)
        
        entries = {}
        for i, (field_name, field_type) in enumerate(fields.items()):
            tk.Label(dialog, text=field_name, bg='#ecf0f1', fg='#2c3e50').grid(row=i, column=0, padx=10, pady=5, sticky='e')
            
            if field_type == "entry":
                entry = tk.Entry(dialog, font=('Arial', 10), bg='white', fg='#2c3e50', relief='solid', bd=1)
                entry.grid(row=i, column=1, padx=10, pady=5, sticky='we')
                entries[field_name] = entry
            elif field_type == "spinbox":
                spinbox = tk.Spinbox(dialog, from_=0, to=100, font=('Arial', 10))
                spinbox.grid(row=i, column=1, padx=10, pady=5, sticky='we')
                entries[field_name] = spinbox
        
        # Style des boutons
        button_frame = tk.Frame(dialog, bg='#ecf0f1')
        button_frame.grid(row=len(fields), columnspan=2, pady=10)
        
        ok_button = tk.Button(button_frame, text="OK", bg='#3498db', fg='white', activebackground='#2980b9')
        ok_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = tk.Button(button_frame, text="Annuler", bg='#e74c3c', fg='white', activebackground='#c0392b')
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        return dialog, entries

    def charger_etudiants(self):
        self.etudiants.clear()
        rows = self.db.fetch_query("SELECT id, nom, prenom, age, email, tel, note1, note2, note3 FROM Stagiaires")
        for row in rows:
            self.etudiants.append(Etudiant(*row))

    def charger_professeurs(self):
        self.professeurs.clear()
        rows = self.db.fetch_query("SELECT id, nom, prenom, tel, matiere FROM Professeur")
        for row in rows:
            self.professeurs.append(Professeur(*row))

    def charger_salles(self):
        self.salles.clear()
        rows = self.db.fetch_query("SELECT nom, numero FROM Salles")
        for row in rows:
            self.salles.append(Salle(*row))

    def create_widgets(self):
        style = {"bg": "#34495e", "fg": "white", "padx": 50, "pady": 8, 
                "font": ('Arial', 10, 'bold'), "relief": "raised", "bd": 2}
        
        actions = [
            ("Ajouter un stagiaire", self.ajouter_etudiant),
            ("Saisir les notes", self.saisir_notes),
            ("Modifier un stagiaire", self.modifier_etudiant),
            ("Rechercher un stagiaire", self.rechercher_etudiant),
            ("Supprimer un stagiaire", self.supprimer_etudiant),
            ("Afficher les résultats", self.afficher_resultats),
            ("Calculer moyenne", self.calcule_moyenne_etudiant),
            ("Afficher tous les stagiaires", self.afficher_etudiants),
            ("Exporter stagiaires JSON", self.exporter_etudiants_json),
            ("Ajouter un professeur", self.ajouter_professeur),
            ("Afficher professeurs", self.afficher_professeurs),
            ("Supprimer professeur", self.supprimer_professeur),
            ("Exporter professeurs JSON", self.exporter_professeurs_json),
            ("Ajouter une salle", self.ajouter_salle),
            ("Afficher salles", self.afficher_salles),
            ("Exporter salles JSON", self.exporter_salles_json),
            ("Quitter", self.root.quit),
        ]
        
        for label, cmd in actions:
            btn = tk.Button(self.root, text=label, command=cmd, **style)
            btn.pack(pady=3)
            # hover 
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#3498db"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#34495e"))

    # === Étudiant ===

    def ajouter_etudiant(self):
        try:
            id = simpledialog.askstring("ID étudiant", "Entrer l'ID :")
            if not id: return
            
            nom = simpledialog.askstring("Nom", "Entrer le nom :")
            if not validate_string(nom): return
            
            prenom = simpledialog.askstring("Prénom", "Entrer le prénom :")
            if not validate_string(prenom): return
            
            age = simpledialog.askinteger("Âge", "Entrer l'âge :")
            if not validate_age(age): return
            
            email = simpledialog.askstring("Email", "Entrer l'email :")
            if not validate_email(email): return
            
            tel = simpledialog.askstring("Téléphone", "Entrer le numéro :")
            if not validate_phone(tel): return
            
            note1 = simpledialog.askfloat("Note 1", "Entrer la première note :") or 0
            if not validate_notes(note1): return
            
            note2 = simpledialog.askfloat("Note 2", "Entrer la deuxième note :") or 0
            if not validate_notes(note2): return
            
            note3 = simpledialog.askfloat("Note 3", "Entrer la troisième note :") or 0
            if not validate_notes(note3): return

            # l'existance de tableaux
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS Stagiaires (
                    id VARCHAR(50) PRIMARY KEY,
                    nom VARCHAR(50),
                    prenom VARCHAR(50), 
                    age INT,
                    email VARCHAR(100),
                    tel VARCHAR(20),
                    note1 FLOAT DEFAULT 0,
                    note2 FLOAT DEFAULT 0,
                    note3 FLOAT DEFAULT 0
                )
            """)

            sql = """INSERT INTO Stagiaires 
                (id, nom, prenom, age, email, tel, note1, note2, note3) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            self.db.execute(sql, (id, nom, prenom, age, email, tel, note1, note2, note3))
            self.etudiants.append(Etudiant(id, nom, prenom, age, email, tel, note1, note2, note3))
            messagebox.showinfo("Succès", "Étudiant ajouté avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {e}")

    def afficher_etudiants(self):
        if not self.etudiants:
            messagebox.showinfo("Info", "Aucun étudiant trouvé.")
        else:
            columns = ("ID", "Nom", "Prénom", "Âge", "Email", "Téléphone", "Note 1", "Note 2", "Note 3", "Moyenne")
            data = [
                (e.id, e.nom, e.prenom, e.age, e.email, e.tel, 
                e.note1, e.note2, e.note3, f"{e.calculer_moyenne():.2f}")
                for e in self.etudiants
            ]
            self.show_info_window("Liste des Étudiants", data, columns)

    def show_info_window(self, title, data_list, columns):
        """Afficher les informations dans un tableau interactif"""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("1600x600")
        window.configure(bg='#f0f0f0')
        
        # Style du tableau
        style = ttk.Style()
        style.theme_use('clam')  
        
        # Configuration du style
        style.configure("Treeview",
            font=('Arial', 10),
            rowheight=30,
            background="#ffffff",
            foreground="#333333",
            fieldbackground="#ffffff",
            bordercolor="#dddddd",
            borderwidth=1)
            
        style.configure("Treeview.Heading",
            font=('Arial', 11, 'bold'),
            background="#3498db",
            foreground="white",
            relief="flat")
            
        style.map("Treeview",
            background=[('selected', '#2980b9')],
            foreground=[('selected', 'white')])
        
        # Cadre principal
        main_frame = ttk.Frame(window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tableau
        tree = ttk.Treeview(main_frame, columns=columns, show="headings", selectmode="browse")
        
        # Configuration des colonnes
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.W)  # Alignement à gauche
        
        # Ajout des données
        for item in data_list:
            tree.insert("", tk.END, values=item)
        
        # Barre de défilement
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Effet de survol
        def on_enter(e):
            tree = e.widget
            item = tree.identify_row(e.y)
            if item:
                tree.tk.call(tree, "tag", "add", "hover", item)
        
        def on_leave(e):
            tree = e.widget
            item = tree.identify_row(e.y)
            if item:
                tree.tk.call(tree, "tag", "remove", "hover", item)
        
        # Configuration du style de survol
        style.configure("Hover.Treeview", background="#f5f5f5")
        tree.tag_configure("hover", background="#f5f5f5")
        
        # Liaison des événements
        tree.bind("<Motion>", on_enter)
        tree.bind("<Leave>", on_leave)
        
        # Bouton Fermer
        ttk.Button(window, text="Fermer", command=window.destroy).pack(pady=10)

    def rechercher_etudiant(self):
        id = simpledialog.askstring("ID", "ID étudiant à rechercher :")
        if not id: return
        
        for e in self.etudiants:
            if str(e.id) == str(id):
                messagebox.showinfo("Étudiant trouvé", e.afficher_infos())
                return
        messagebox.showinfo("Introuvable", "Aucun étudiant trouvé avec cet ID.")

    def supprimer_etudiant(self):
        id = simpledialog.askstring("ID", "ID étudiant à supprimer :")
        if not id: return
        
        for e in self.etudiants:
            if str(e.id) == str(id):
                if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cet étudiant?"):
                    self.db.execute("DELETE FROM Stagiaires WHERE id = %s", (id,))
                    self.etudiants.remove(e)
                    messagebox.showinfo("Supprimé", "Étudiant supprimé avec succès.")
                return
        messagebox.showinfo("Introuvable", "Aucun étudiant trouvé avec cet ID.")

    def saisir_notes(self):
        id = simpledialog.askstring("ID", "ID étudiant :")
        if not id: return
        
        for e in self.etudiants:
            if str(e.id) == str(id):
                n1 = simpledialog.askfloat("Note 1", f"Note 1 actuelle: {e.note1}\nEntrez nouvelle note 1 :")
                if n1 is not None and not validate_notes(n1): return
                
                n2 = simpledialog.askfloat("Note 2", f"Note 2 actuelle: {e.note2}\nEntrez nouvelle note 2 :")
                if n2 is not None and not validate_notes(n2): return
                
                n3 = simpledialog.askfloat("Note 3", f"Note 3 actuelle: {e.note3}\nEntrez nouvelle note 3 :")
                if n3 is not None and not validate_notes(n3): return
                
                if n1 is not None: e.note1 = n1
                if n2 is not None: e.note2 = n2
                if n3 is not None: e.note3 = n3
                
                # Mise à jour en base de données
                sql = "UPDATE Stagiaires SET note1=%s, note2=%s, note3=%s WHERE id=%s"
                self.db.execute(sql, (e.note1, e.note2, e.note3, id))
                messagebox.showinfo("Succès", "Notes mises à jour avec succès!")
                return
        messagebox.showinfo("Introuvable", "Étudiant non trouvé.")

    def afficher_resultats(self):
        id = simpledialog.askstring("ID", "ID étudiant :")
        if not id: return
        
        for e in self.etudiants:
            if str(e.id) == str(id):
                # Création d'une fenêtre dédiée
                notes_window = tk.Toplevel(self.root)
                notes_window.title(f"le résultat de {e.prenom} {e.nom}")
                notes_window.geometry("400x300")
                notes_window.configure(bg='#2c3e50')
                notes_window.resizable(False, False)
                
                # Style CSS-like
                title_style = {'font': ('Arial', 14, 'bold'), 'bg': '#2c3e50', 'fg': 'white'}
                label_style = {'font': ('Arial', 11), 'bg': '#34495e', 'fg': 'white', 'anchor': 'w'}
                note_style = {'font': ('Arial', 11, 'bold'), 'bg': '#34495e', 'fg': '#3498db'}
                avg_style = {'font': ('Arial', 12, 'bold'), 'bg': '#2c3e50', 'fg': '#2ecc71'}
                
                # Titre
                tk.Label(notes_window, text=f"le résultat de {e.prenom} {e.nom}", **title_style).pack(pady=10)
                
                # Frame pour les notes
                notes_frame = tk.Frame(notes_window, bg='#34495e', padx=20, pady=10)
                notes_frame.pack(pady=5, fill='x')
                
                # Affichage des notes
                tk.Label(notes_frame, text="Note 1:", **label_style).grid(row=0, column=0, sticky='w')
                tk.Label(notes_frame, text=f"{e.note1:.2f}", **note_style).grid(row=0, column=1, sticky='e')
                
                tk.Label(notes_frame, text="Note 2:", **label_style).grid(row=1, column=0, sticky='w')
                tk.Label(notes_frame, text=f"{e.note2:.2f}", **note_style).grid(row=1, column=1, sticky='e')
                
                tk.Label(notes_frame, text="Note 3:", **label_style).grid(row=2, column=0, sticky='w')
                tk.Label(notes_frame, text=f"{e.note3:.2f}", **note_style).grid(row=2, column=1, sticky='e')
                
                # Séparateur
                tk.Frame(notes_window, height=2, bg='#3498db').pack(fill='x', pady=10)
                
                # Moyenne
                moyenne = e.calculer_moyenne()
                status = "Admis" if moyenne >= 10 else "Non admis"
                status_color = '#2ecc71' if moyenne >= 10 else '#e74c3c'
                
                avg_frame = tk.Frame(notes_window, bg='#2c3e50')
                avg_frame.pack(fill='x', padx=20, pady=5)
                
                tk.Label(avg_frame, text="Moyenne:", **label_style).pack(side='left')
                tk.Label(avg_frame, text=f"{moyenne:.2f}", **avg_style).pack(side='left', padx=10)
                
                # Statut
                tk.Label(notes_window, text=f"Statut: {status}", 
                        font=('Arial', 12, 'bold'), 
                        bg='#2c3e50', fg=status_color).pack(pady=10)
                
                # Bouton Fermer
                tk.Button(notes_window, text="Fermer", command=notes_window.destroy,
                        bg='#e74c3c', fg='white', activebackground='#c0392b',
                        font=('Arial', 10, 'bold'), padx=20).pack(pady=10)
                
                return
        
        messagebox.showinfo("Introuvable", "Aucun étudiant trouvé.", parent=self.root)

    def calcule_moyenne_etudiant(self):
        id = simpledialog.askstring("ID", "ID étudiant :")
        if not id: return
        
        for e in self.etudiants:
            if str(e.id) == str(id):
                moy = e.calculer_moyenne()
                status = "Admis" if moy >= 10 else "Non admis"
                messagebox.showinfo("Moyenne", f"Étudiant: {e.prenom} {e.nom}\nMoyenne: {moy:.2f}\nStatut: {status}")
                return
        messagebox.showinfo("Introuvable", "Étudiant non trouvé.")

    def modifier_etudiant(self):
        id = simpledialog.askstring("ID", "ID étudiant à modifier :")
        if not id: return
        
        for e in self.etudiants:
            if str(e.id) == str(id):
                nom = simpledialog.askstring("Nom", f"Nom actuel: {e.nom}\nNouveau nom :") or e.nom
                if not validate_string(nom): return
                
                prenom = simpledialog.askstring("Prénom", f"Prénom actuel: {e.prenom}\nNouveau prénom :") or e.prenom
                if not validate_string(prenom): return
                
                age = simpledialog.askinteger("Âge", f"Âge actuel: {e.age}\nNouvel âge :") or e.age
                if not validate_age(age): return
                
                email = simpledialog.askstring("Email", f"Email actuel: {e.email}\nNouvel email :") or e.email
                if not validate_email(email): return
                
                tel = simpledialog.askstring("Téléphone", f"Téléphone actuel: {e.tel}\nNouveau téléphone :") or e.tel
                if not validate_phone(tel): return

                e.nom, e.prenom, e.age, e.email, e.tel = nom, prenom, age, email, tel
                sql = """UPDATE Stagiaires SET nom=%s, prenom=%s, age=%s, email=%s, tel=%s WHERE id=%s"""
                self.db.execute(sql, (nom, prenom, age, email, tel, id))
                messagebox.showinfo("Succès", "Étudiant modifié avec succès.")
                return
        messagebox.showinfo("Introuvable", "Étudiant non trouvé.")

    def exporter_etudiants_json(self):
        try:
            # Créer le dossier export s'il n'existe pas
            import os
            if not os.path.exists("export"):
                os.makedirs("export")
                
            data = [{
                "id": e.id, "nom": e.nom, "prenom": e.prenom, "age": e.age,
                "email": e.email, "tel": e.tel, "note1": e.note1, "note2": e.note2, "note3": e.note3,
                "moyenne": e.calculer_moyenne()
            } for e in self.etudiants]
            
            with open("export/etudiants_export.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Exporté", "Étudiants exportés en JSON dans le dossier 'export'.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {e}")

    # === Professeur ===

    def ajouter_professeur(self):
        try:
            id = simpledialog.askstring("ID", "ID professeur :")
            if not id: return
            
            nom = simpledialog.askstring("Nom", "Nom professeur :")
            if not validate_string(nom): return
            
            prenom = simpledialog.askstring("Prénom", "Prénom professeur :")
            if not validate_string(prenom): return
            
            tel = simpledialog.askstring("Téléphone", "Téléphone professeur :")
            if not validate_phone(tel): return
            
            matiere = simpledialog.askstring("Matière", "Matière enseignée :")
            if not matiere: return

            # Créer la table si elle n'existe pas
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS Professeur (
                    id VARCHAR(50) PRIMARY KEY,
                    nom VARCHAR(50),
                    prenom VARCHAR(50),
                    tel VARCHAR(20),
                    matiere VARCHAR(100)
                )
            """)

            sql = "INSERT INTO Professeur (id, nom, prenom, tel, matiere) VALUES (%s, %s, %s, %s, %s)"
            self.db.execute(sql, (id, nom, prenom, tel, matiere))
            self.professeurs.append(Professeur(id, nom, prenom, tel, matiere))
            messagebox.showinfo("Succès", "Professeur ajouté avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {e}")

    def afficher_professeurs(self):
        if not self.professeurs:
            messagebox.showinfo("Info", "Aucun professeur trouvé.")
        else:
            columns = ("ID", "Nom", "Prénom", "Téléphone", "Matière")
            data = [
                (p.id, p.nom, p.prenom, p.tel, p.matiere)
                for p in self.professeurs
            ]
            self.show_info_window("Liste des Professeurs", data, columns)

    def supprimer_professeur(self):
        id = simpledialog.askstring("ID", "ID professeur à supprimer :")
        if not id: return
        
        for p in self.professeurs:
            if str(p.id) == str(id):
                if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce professeur?"):
                    self.db.execute("DELETE FROM Professeur WHERE id = %s", (id,))
                    self.professeurs.remove(p)
                    messagebox.showinfo("Supprimé", "Professeur supprimé avec succès.")
                return
        messagebox.showinfo("Introuvable", "Professeur non trouvé.")

    def exporter_professeurs_json(self):
        try:
            import os
            if not os.path.exists("export"):
                os.makedirs("export")
                
            data = [{
                "id": p.id, "nom": p.nom, "prenom": p.prenom, "tel": p.tel, "matiere": p.matiere
            } for p in self.professeurs]
            
            with open("export/professeurs.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Exporté", "Professeurs exportés en JSON dans le dossier 'export'.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {e}")

    # === Salle ===

    def ajouter_salle(self):
        try:
            nom = simpledialog.askstring("Nom", "Nom de la salle :")
            if not nom: return
            
            numero = simpledialog.askinteger("Numéro", "Numéro de la salle :")
            if not numero: return

            # Créer la table si elle n'existe pas
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS Salles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nom VARCHAR(50),
                    numero INT
                )
            """)

            sql = "INSERT INTO Salles (nom, numero) VALUES (%s, %s)"
            self.db.execute(sql, (nom, numero))
            self.salles.append(Salle(nom, numero))
            messagebox.showinfo("Succès", "Salle ajoutée avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {e}")

    def afficher_salles(self):
        if not self.salles:
            messagebox.showinfo("Info", "Aucune salle trouvée.")
        else:
            columns = ("Nom", "Numéro")
            data = [
                (s.nom, s.numero)
                for s in self.salles
            ]
            self.show_info_window("Liste des Salles", data, columns)

    def exporter_salles_json(self):
        try:
            import os
            if not os.path.exists("export"):
                os.makedirs("export")
                
            data = [{"nom": s.nom, "numero": s.numero} for s in self.salles]
            with open("export/salles.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Exporté", "Salles exportées en JSON dans le dossier 'export'.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {e}")
from tkinter import messagebox

def validate_string(string):
    if not string.isalpha():
        messagebox.showerror("Erreur", "Le champ doit être composé uniquement de lettres.")
        return False
    return True

def validate_age(age):
    if not (18 <= age <= 30):
        messagebox.showerror("Erreur", "L'âge doit être entre 18 et 30.")
        return False
    return True

def validate_email(email):
    if "@" not in email or not email.endswith(".com"):
        messagebox.showerror("Erreur", "Email invalide.")
        return False
    return True

def validate_phone(tel):
    if not tel.isdigit():
        messagebox.showerror("Erreur", "Le numéro de téléphone doit être un entier.")
        return False
    return True

def validate_notes(note):
    if not (0 <= note <= 20):
        messagebox.showerror("Erreur", "Les notes doivent être entre 0 et 20.")
        return False
    return True

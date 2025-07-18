class Personne:
    nombre = 0

    def __init__(self, id, nom, prenom, tel):
        self.__id = id
        self.nom = nom
        self.prenom = prenom
        self.__tel = tel
        Personne.nombre += 1

    @property
    def id(self):
        return self.__id

    @property
    def tel(self):
        return self.__tel

    @tel.setter
    def tel(self, value):
        self.__tel = value


class Etudiant(Personne):
    def __init__(self, id, nom, prenom, age, email, tel, note1=0, note2=0, note3=0):
        super().__init__(id, nom, prenom, tel)
        self.age = age
        self.__email = email
        self.note1 = note1
        self.note2 = note2
        self.note3 = note3

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    def afficher_infos(self):
        return (f"ID : {self.id}, Nom : {self.nom}, Prénom : {self.prenom}, "
                f"Âge : {self.age}, Email : {self.email}, Téléphone : {self.tel}\n"
                f"Notes : {self.note1}, {self.note2}, {self.note3}")

    def calculer_moyenne(self):
        notes = [self.note1, self.note2, self.note3]
        return sum(notes) / len(notes)


class Professeur(Personne):
    def __init__(self, id, nom, prenom, tel, matiere):
        super().__init__(id, nom, prenom, tel)
        self.matiere = matiere

    def afficher_infos(self):
        return (f"ID : {self.id}, Nom : {self.nom}, Prénom : {self.prenom}, "
                f"Téléphone : {self.tel}, Matière : {self.matiere}")

from django.db import models


# Create your models here.
class Espece(models.Model):
    nom_commun = models.CharField(max_length=250)
    nom_scientifique = models.CharField(max_length=250, null=True)  # si pas d'entree, valeur nulle par défaut

    def __str__(self):
        """permet de retourner la valeur souhaite dans admin au lieu de objet 0001"""
        return self.nom_commun

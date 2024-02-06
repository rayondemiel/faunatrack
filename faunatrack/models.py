from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from faunatrack.validators import validate_latitude

# Create your models here.
class Espece(models.Model):
    STATUT = [
        ("DISPARU", "En voie de disparition"),
        ("DANGER", "En danger"),
        ("PROTEGE", "Protégé"),
        ("INCONNU", "On sait pas!")
    ]

    nom_commun = models.CharField(max_length=250)
    nom_scientifique = models.CharField(max_length=250, null=True)  # si pas d'entree, valeur nulle par défaut
    statut = models.CharField(max_length=250, choices=STATUT, default="INCONNU")

    def __str__(self):
        """permet de retourner la valeur souhaite dans admin au lieu de objet 0001"""
        return self.nom_commun


class Project(models.Model):
    ETAT = [
        ("ACT", "PROJET_ACTIF"),
        ("INACT", "PROJET_INACTIF")
    ]
    nom = models.CharField(max_length=250)
    description = models.TextField()
    date_debut = models.DateField(auto_now_add=True)  # ajouter automatique à la date d'aujourd'hui
    etat = models.CharField(max_length=15, choices=ETAT, default="INACT")
    #especes_observées = models.ManyToManyField(Espece, through=Observation)
    observations = models.ManyToManyField("faunatrack.Observation", related_name="projets", null=True) # pour éviter problème recursivite comme après

    def __str__(self):
        """permet de retourner la valeur souhaite dans admin au lieu de objet 0001"""
        return f"{self.nom} ({self.date_debut})"


class Scientifique(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.PROTECT, related_name="scientifique",
                                verbose_name="Profil Scientifique")
    specialite = models.CharField(max_length=250, null=True, blank=True)
    Institution = models.CharField(max_length=250, default="CNRS", blank=True)

    def __str__(self):
        """permet de retourner la valeur souhaite dans admin au lieu de objet 0001"""
        return f"{self.user.username}, spécialiste en {self.specialite}"


class Observation(models.Model):
    date_observation = models.DateTimeField(blank=True, null=True)
    espece = models.ForeignKey(Espece, related_name="observations", on_delete=models.CASCADE)
    quantite = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, validators=[validate_latitude], help_text="je suis l'aide") # own validator
    longitude = models.DecimalField(max_digits=9, decimal_places=6, validators=[MaxValueValidator(limit_value=180), MinValueValidator(limit_value=-180)])
    notes = models.TextField(default="Pas de notes")
    photos = models.ImageField(upload_to="faunatrack/static/observations_photos/", null=True, blank=True)
    scientifique = models.ForeignKey(Scientifique, related_name="observation", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Observation: {self.espece.nom_commun}, {self.date_observation}"

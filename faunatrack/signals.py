from django.db.models.signals import post_save, pre_save
from faunatrack.models import Observation, Scientifique, Espece
from django.dispatch import receiver
from django.contrib.auth.models import User, Permission
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=Observation)
def update_espece_statut(sender, instance, created, **kwargs):
    """
    fonction pour actualise automatiquement le statut de l'espece des qu'il
    la methode dit que quand recoit un signal de reception du modele Observation dans base de données actualise le statut
    sender ->
    instance ->
    created -> dit que si c'est une creation
    kwargs -> ensemble de parametre
    """
    espece: Espece = instance.espece # typage pour aider autocompletion
    observations_espece = Observation.objects.filter(espece=espece).aggregate(total_espece=Sum("quantite"))
    nb_espece = observations_espece["total_espece"]
    if nb_espece == 0:
        espece.statut = 'INCONNU'
    elif nb_espece <= 10:
        espece.statut = "DISPARU"
    elif nb_espece <= 100:
        espece.statut = "DANGER"
    else:
        espece.statut = "PROTEGE"

    espece.save()

@receiver(post_save, sender=Scientifique)
def add_scientifique_permissions(sender, instance, created, **kwargs):
    """ des qu'un utilisateur scientifique est créé on lui ajoute toutes les permission liées à faunatrack, mais on lui autorise pas d'ajouter un scientifique"""
    user = instance.user
    if created:
        content_type_ids = []
        content_type_ids.append(ContentType.objects.get(model='scientifique').id)
        permissions = Permission.objects.filter(content_type__app_label="faunatrack").exclude(
            content_type_id__in=content_type_ids) #__in permet de regarder directement dans une liste
        for permission in permissions:
            user.user_permissions.add(permission)
        user.save()

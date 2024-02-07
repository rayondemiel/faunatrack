from django.test import TestCase
from faunatrack.signals import update_espece_statut
from django.db.models.signals import post_save
from faunatrack.models import Observation, Espece

from datetime import datetime

# Create your tests here.
class EspecesStatus(TestCase):

    def setUp(self):
        post_save.connect(update_espece_statut, sender=Observation)
        self.espece = Espece.objects.create(nom_commun='Lion') # on cree une espece pour lateste

    def test_espece_status_change(self):
        espece_udpated = Espece.objects.get(id=self.espece.id)
        self.assertEqual(espece_udpated.statut, "INCONNU")

        Observation.objects.create(espece=self.espece, quantite=3, latitude=5, longitude=7, date_observation=datetime.strptime("01/01/2024", "%d/%m/%Y"))
        espece_udpated = Espece.objects.get(id=self.espece.id)
        self.assertEqual(espece_udpated.statut, "DISPARU")

        Observation.objects.create(espece=self.espece, quantite=7, latitude=5, longitude=7,
                                   date_observation=datetime.strptime("01/01/2024", "%d/%m/%Y"))
        Observation.objects.create(espece=self.espece, quantite=15, latitude=5, longitude=7,
                                   date_observation=datetime.strptime("01/01/2024", "%d/%m/%Y"))

        espece_udpated = Espece.objects.get(id=self.espece.id)
        self.assertEqual(espece_udpated.statut, "DANGER")

        Observation.objects.create(espece=self.espece, quantite=3, latitude=5, longitude=7,
                                   date_observation=datetime.strptime("01/01/2024", "%d/%m/%Y"))
        Observation.objects.create(espece=self.espece, quantite=7, latitude=5, longitude=7,
                                   date_observation=datetime.strptime("01/01/2024", "%d/%m/%Y"))
        Observation.objects.create(espece=self.espece, quantite=150, latitude=5, longitude=7,
                                   date_observation=datetime.strptime("01/01/2024", "%d/%m/%Y"))
        espece_udpated = Espece.objects.get(id=self.espece.id)
        self.assertEqual(espece_udpated.statut, "PROTEGE")

    def tearDown(self):
        post_save.disconnect(update_espece_statut, sender=Observation)
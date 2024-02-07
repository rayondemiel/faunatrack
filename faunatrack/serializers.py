from rest_framework import serializers
from faunatrack.models import Espece, Observation, Project

class EspeceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espece
        fields = '__all__'

"""class EspeceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espece
        field = '__all__'"""

class ObservationSerializer(serializers.ModelSerializer):
    espece_detail = EspeceSerializer(source="espece", read_only=True) #ob reutilise nos serialisezs

    class Meta:
        model = Observation
        fields = ['id', 'date_observation', 'latitude', 'longitude', 'espece_detail', 'espece', 'quantite']

class ProjectSerializer(serializers.ModelSerializer): #source == attribut de notre model (voir Meta)
    observations_details = ObservationSerializer(source="observations", read_only=True, many=True) # source est representation # faut preciser que c'est un Many-to-Many
    class Meta:
        model = Project
        fields = ['observations_details', 'slug']
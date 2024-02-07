from rest_framework import viewsets, generics
from faunatrack.models import Espece, Observation, Project
from faunatrack.serializers import EspeceSerializer, ObservationSerializer, ProjectSerializer

class EspeceViewSet(viewsets.ModelViewSet):
    queryset = Espece.objects.all()
    serializer_class = EspeceSerializer # pour integrer le serialiszer

class ObservationListCreate(viewsets.ViewSetMixin, generics.ListCreateAPIView): #il faut ViewSetMixin
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(observations__in=Observation.objects.filter(latitude__gte=50)) # la obervationsid __ dans liste (la requere avec latitutde plus grand que 50
    serializer_class = ProjectSerializer
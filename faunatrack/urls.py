from django.urls import path
from faunatrack.views import ProjetListView, EspeceListView, ProjetView, ProjetCreateView, EspeceCreateView, ProjetUpdateView, ProjetDeleteView, ObservationCreateView

urlpatterns = [
    path("projets/", ProjetListView.as_view(), name="projet_list"),
    path("especes/", EspeceListView.as_view(), name="espece_list"),
    path("projets/<int:pk>/", ProjetView.as_view(), name="projet"),
    path("projets/<int:pk>/update", ProjetUpdateView.as_view(), name="projet_update"),
    path("projets/create/", ProjetCreateView.as_view(), name="create_projet"),
    path("especes/create/", EspeceCreateView.as_view(), name="create_espece"),
    path("observations/create/", ObservationCreateView.as_view(), name="create_observation"),
    path("especes/<int:pk>/delete", ProjetDeleteView.as_view(), name="delete_project")
]
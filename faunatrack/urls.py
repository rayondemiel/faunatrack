from django.urls import path
from faunatrack.views import ProjetListView

urlpatterns = [
    path("projets/", ProjetListView.as_view(), name="projet_list")

]
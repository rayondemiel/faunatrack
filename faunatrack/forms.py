from django.forms import ModelForm
from faunatrack.models import Project, Espece, Observation
from faunatrack.validators import validate_latitude
from django import forms

class FaunaTrackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "border rounded-lg focus:ring-blue-500 w-full p-2.5"
class ProjetForm(FaunaTrackForm):
    class Meta:
        model = Project
        fields = ["nom", "description", "etat", "observations"]

class EspeceForm(FaunaTrackForm):
    class Meta:
        model = Espece
        fields = "__all__" # je recuperer tous les champs

class ObservationForm(FaunaTrackForm):
    class Meta:
        model = Observation
        fields = ["latitude", "longitude", "quantite", "espece", "date_observation"]
        widgets = {
            "date_observation": forms.widgets.DateTimeInput(
                attrs={"type": "datetime-local"})
        }
    quantite = forms.IntegerField(
        label = "Nombre d'espèces observée",
        help_text="Comptez bien!",
        min_value=1,
        max_value=100
    )

    def clean_latitude(self):
        latitude = self.cleaned_data.get("latitude") # vdjango si pas de probleme de securité
        validate_latitude(latitude)
        return latitude

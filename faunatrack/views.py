from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from faunatrack.models import Project, Espece, Observation, Scientifique
from faunatrack.forms import ProjetForm, EspeceForm, ObservationForm


# Create your views here.
def home(request):
    return render(request, template_name="base.html")

@login_required()
def confirm_delete(request, model_name, pk):
    "global method delete. C'est pas la meilleure methode, plus facile à maintenir "
    if request.method=="POST":
        model = apps.get_model(app_label="faunatrack", model_name=model_name)
        object_to_delete = model.objects.get(id=pk)
        object_to_delete.delete()
        return redirect(f"{model_name}_list") # parcontre faut
    return render(request, "delete.html", { "model": model_name})


"""def projet_list(request):
    "methode specifique pour afficher une liste. S'utilise quand on a plusieurs besoir"
    projets = Project.objects.prefetch_related() -> prechargement des relations pour perdformance
    projets = Project.objects.filter(observation__nom="Ours") -> utilise double underscore por faire la jointure et chercher dans l'autre base
    projets = Project.objects.filter(nom="Pythagore")
    return render(request, "projet_list", {"projets": projets})"""

class ProjetListView(ListView):
    "methode generaliste pour afficher une liste sans specificité"
    model = Project # sera le nom miniscule dans html
    template_name = "projet_list.html"
    #queryset = Project. # c'est pour definir notre query de base (mais pas forcement utile), depend utilsaition

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        "méthode pour sucharger ^pour spécifier certains comportements"
        context = super().get_context_data(**kwargs)
        context["ma_var"] = "youpi"
        return context

class ProjetView(DetailView):
    model = Project
    template_name = "projet.html"
    extra_context = {"truc": "ma var"} # pour faire comme get_context_data

class ProjetCreateView(LoginRequiredMixin, CreateView):
    form_class = ProjetForm #import du model de form
    model = Project #import du modele
    template_name = "projet_create.html"
    success_url = reverse_lazy("projet_list") #Retour a cette url quand succes

class ProjetUpdateView(UserPassesTestMixin, UpdateView):
    model = Project
    fields = "__all__" # pour faire des update sur tout si on veut pas faire de custom
    template_name = "projet_create.html"
    success_url = reverse_lazy("projet_list")

    """def test_func(self) -> bool | None:
        "pour regarder si l'user a deja creer un truc, sinon ne peut pas le faire. Ne marche pas ..."
        user = self.request.user
        profil_scientifique = Scientifique.objects.filter(user__username=user)
        if len(profil_scientifique.observation.all()) <=0:
            return False
        return True"""

class ProjetDeleteView(DeleteView):
    "detele view for projetct"
    model = Project
    template_name = "delete.html"
    success_url = reverse_lazy("projet_list")
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        "le mieux pour supprimer avec le meme template"
        context = super().get_context_data(**kwargs)
        context["model"] = "project"
        return context

class EspeceListView(ListView):
    model = Espece
    template_name = "espece_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        "méthode pour sucharger ^pour spécifier certains comportements"
        context = super().get_context_data(**kwargs)
        context["nb_espece"] = self.model.objects.count()
        context["observations"] = Observation.objects.prefetch_related()
        return context

class EspeceCreateView(UserPassesTestMixin, CreateView):
    form_class = EspeceForm
    model = Espece
    template_name = "projet_create.html"
    success_url = reverse_lazy("espece_list")

    """def test_func(self) -> bool | None:
        if self.request.user.has_perm('faunatrack.add_espece'):
            return True"""
class ObservationListView(ListView):
    model = Observation
    template_name = ""

@method_decorator(permission_required("faunatrack.add_observation", raise_exception=True), name="dispatch")
class ObservationCreateView(CreateView):
    form_class = ObservationForm
    model = Observation
    template_name = "observation_create.html"
    success_url = reverse_lazy('espece_list')
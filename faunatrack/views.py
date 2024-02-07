from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum

from faunatrack.models import Project, Espece, Observation, Scientifique
from faunatrack.forms import ProjetForm, EspeceForm, ObservationForm


# Create your views here.
def home(request):
    """Si l utilisateur n'est pas connecte lui retourne vers connexion et si c'et o va dans home"""
    if request.user.is_authenticated:
        especes = Espece.objects.all()
        table = [(espece.nom_commun, Observation.objects.filter(espece=espece).aggregate(total=Sum("quantite"))["total"], espece.get_statut_display()) for espece in especes ]
        return render(request, context={"table": table}, template_name="base.html")
    return redirect("login")

def test_function(request):
    content_type_ids = []
    content_type_ids.append(ContentType.objects.get(model='scientifique').id)
    permissions = Permission.objects.filter(content_type__app_label="faunatrack").exclude(content_type_id__in=content_type_ids)
    print(permissions)
    return redirect("home")

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

class AuthorizedView(LoginRequiredMixin, PermissionRequiredMixin):
    pass

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

class ProjetCreateView(UserPassesTestMixin, AuthorizedView, SuccessMessageMixin, CreateView):
    form_class = ProjetForm #import du model de form
    model = Project #import du modele
    template_name = "projet_create.html"
    permission_required = "faunatrack.add_project"
    success_url = reverse_lazy("projet_list") #Retour a cette url quand succes
    success_message = "Projet créé !"

    def test_func(self) -> bool | None:
        """pour regarder si l'user a deja creer un truc et on retourne les trucs qu'il a fait, sinon ne peut pas le
        faire. """
        try:
            profile_scientifique = self.request.user.scientifique
            return profile_scientifique and profile_scientifique.observation.all()
        except Scientifique.DoesNotExist:
            return False

    def handle_no_permission(self):
        """Pour retourner message avec fonction specifique sans permission. si je ne suis pas authentifier
        -> je renvoie la fonction parente. SI je suis pas authentifier mais pas la
        -> il faut avoir validé test_fund() donc avoir enrigstrer des objservation"""
        # faut faire le check sinon on arriv à 403
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        # je fais mon message d'erreur si pas la permission
        messages.error(self.request, "Accès non autorisé, vous n'êtes pas sicentifiques !", extra_tags="text-red-500")
        return redirect('home')

class ProjetUpdateView(UpdateView):
    model = Project
    fields = "__all__" # pour faire des update sur tout si on veut pas faire de custom
    template_name = "projet_create.html"
    success_url = reverse_lazy("projet_list")

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(self.request, message="Projet correctement mis à jours")
        return form


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
class ObservationCreateView(SuccessMessageMixin, CreateView):
    form_class = ObservationForm
    model = Observation
    template_name = "observation_create.html"
    success_url = reverse_lazy('espece_list')
    success_message = "Observation créée"

    def form_valid(self, form):
        """permet de dire automatiquement que le scientifique loggé est le champs scientifique à remplir dans le formulaire"""
        form.instance.scientifique = self.request.user.scientifique
        messages.success(self.request, message="Projet correctement mis à jours")
        return super().form_valid(form)
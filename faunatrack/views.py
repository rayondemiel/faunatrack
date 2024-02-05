from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from faunatrack.models import Project

# Create your views here.
def hello_world(request):
    return render(request, template_name="base.html")

class ProjetListView(ListView):
    model = Project
    template_name = "projet_list.html"
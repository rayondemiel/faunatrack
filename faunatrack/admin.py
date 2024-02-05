from django.contrib import admin
from faunatrack.models import Espece

# Register your models here.
@admin.register(Espece)
class EspeceAdmin(admin.ModelAdmin):
    list_display = ["nom_commun", "nom_scientifique"]
    search_fields = ["nom_commun"] # permet de rechercher par ce biais
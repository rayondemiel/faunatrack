from django.contrib import admin
from faunatrack.models import Espece, Project, Observation, Scientifique


class MonAdminFaunatrack(admin.AdminSite):
    """Custom admin site"""
    site_header = "Faunatrack Administration"
    site_title = "Faunatrack Administration"
    index_title = "Welcome toFaunatrack Administration"
    """def get_app_list(self, request, app_label=None):
        
        Return a sorted list of all the installed apps that have been
        registered in this site.
        
        # Sort the apps alphabetically.
        app_list = super().get_app_list(request)
        return sorted(app_list, key=lambda x: x["name"])"""


admin_faunatrack = MonAdminFaunatrack(name='admin_faunatrack')


# Register your models here.
@admin.register(Espece)
class EspeceAdmin(admin.ModelAdmin):
    list_display = ["nom_commun", "nom_scientifique"]
    search_fields = ["nom_commun"]  # permet de rechercher par ce biais


@admin.register(Project)
class ProjetAdmin(admin.ModelAdmin):
    pass


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    pass


@admin.register(Scientifique)
class ScientifiqueAdmin(admin.ModelAdmin):
    pass

# pour site admin faunatrack car possible avec decorateur
admin_faunatrack.register(Espece)
admin_faunatrack.register(Project)
admin_faunatrack.register(Observation)
admin_faunatrack.register(Scientifique)

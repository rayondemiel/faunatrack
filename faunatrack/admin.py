from django.contrib import admin
from faunatrack.models import Espece, Project, Observation, Scientifique
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields


class EspeceExportResource(resources.ModelResource):
    nom_commun = fields.Field(attribute="nom_commun", column_name="nom_commun")
    nom_scientifique = fields.Field(attribute="nom_scientifique", column_name="nom_scientifique")
    statut = fields.Field(attribute="statut", column_name="Statut de l'espece")
    class Meta: #definir modele et champs
        model = Espece
        fields = ("id", "nom_commun", "nom_scientifique", "statut")
        skip_unchanged = True

class ObservationInlineAdmin(admin.TabularInline):
    model = Observation
    extra = 1

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
class EspeceAdmin(ImportExportModelAdmin):
    list_display = ["nom_commun", "nom_scientifique"]
    search_fields = ["nom_commun"]  # permet de rechercher par ce biais

    #pour ajouter des observation rapidement
    inlines = [ObservationInlineAdmin]

    def get_export_resource_classes(self):
        return [EspeceExportResource]


@admin.register(Project)
class ProjetAdmin(admin.ModelAdmin):
    pass


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "espece", "date_observation")
    list_filter = ["espece__nom_commun"]
    search_fields = ["espece__nom_commun", "date_observation", "scientifique__user_username"]
    ordering = ["espece"]
    list_editable = ["espece"]
    actions = ["marquer_comme_critique"]

    # url admin:faunatrack_marquer_comme_critique
    def marquer_comme_critique(self, request, queryset):
        for observation in queryset:
            projets = observation.projets.all()
            for projet in projets:
                projet.description = "CRITIQUE - " + projet.description
                projet.save()
        self.message_user(request, "projet marqué comme critique!")

    marquer_comme_critique.short_description = "Marquer le projet comme critique"

@admin.register(Scientifique)
class ScientifiqueAdmin(admin.ModelAdmin):
    pass

# pour site admin faunatrack car possible avec decorateur (faut le modele et la classe
admin_faunatrack.register(Espece, EspeceAdmin)
admin_faunatrack.register(Project, ProjetAdmin)
admin_faunatrack.register(Observation, ObservationAdmin)
admin_faunatrack.register(Scientifique, ScientifiqueAdmin)

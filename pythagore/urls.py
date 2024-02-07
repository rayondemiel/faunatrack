"""
URL configuration for pythagore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from faunatrack.admin import admin_faunatrack
from faunatrack import views as fauna_views
from faunatrack import api_views as api_faunatrack_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# API uRL
router.register(r'especes', api_faunatrack_views.EspeceViewSet) # nom de la route pour cette classe
router.register(r'observations', api_faunatrack_views.ObservationListCreate)
router.register(r'project_50', api_faunatrack_views.ProjectViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('faunatrack_admin/', admin_faunatrack.urls),
    path('', fauna_views.home, name='home'),
    path('test/', fauna_views.test_function, name='test'),
    path('faunatrack/', include("faunatrack.urls")),
    path('accounts/', include("django.contrib.auth.urls")),
    path('api/', include(router.urls))
]

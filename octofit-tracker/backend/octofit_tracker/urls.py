"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TeamViewSet, ActivityViewSet, LeaderboardViewSet, WorkoutViewSet, api_root
import os

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'workouts', WorkoutViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'leaderboard', LeaderboardViewSet)

def codespace_api_root(request, format=None):
    codespace_name = os.environ.get('CODESPACE_NAME')
    base_url = request.build_absolute_uri('/')
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev/api/"
    else:
        base_url = request.build_absolute_uri('/api/')
    return api_root(request._request, format=format) if hasattr(request, '_request') else api_root(request, format=format)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', codespace_api_root, name='api-root'),
    path('', include(router.urls)),
]

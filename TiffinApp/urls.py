from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from apps.accounts.views import CreateEmailUserViewSet

router = routers.DefaultRouter()

router.register('create-user', CreateEmailUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]

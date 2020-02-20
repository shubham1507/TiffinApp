from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from apps.accounts.views import CreateEmailUserViewSet
from django.urls import path

# def trigger_error(request):
#     division_by_zero = 1 / 0

router = routers.DefaultRouter()

router.register('create-user', CreateEmailUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('sentry-debug/', trigger_error),
]

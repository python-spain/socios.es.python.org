from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from pythonspain.partners.api import PartnerViewSet


app_name = "api_v1"

router = routers.DefaultRouter()
router.register(r"partners", PartnerViewSet)

urlpatterns = [path("", include(router.urls))]

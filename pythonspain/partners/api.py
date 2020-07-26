from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_condition import Or

from pythonspain.core.api.permissions import AllowCreations

from .models import Partner
from .serializers import PartnerSerializer


class PartnerViewSet(ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [Or(IsAuthenticated, AllowCreations)]

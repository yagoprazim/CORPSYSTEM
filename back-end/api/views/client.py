from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.models.client import Client
from api.serializers.client import ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]



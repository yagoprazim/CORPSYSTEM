from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models.vendor import Vendor
from api.serializers.vendor import VendorSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

class UserVendorDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            serializer = VendorSerializer(user.vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({"error": "You are not registered as a vendor"}, status=404)


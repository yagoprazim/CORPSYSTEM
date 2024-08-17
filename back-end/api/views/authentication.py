from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import login, authenticate, logout

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        if user:
            login(request, user)
        return response

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        logout(request)
        return Response({'success': 'User logged out successfully.'})
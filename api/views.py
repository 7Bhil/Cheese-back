from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.db.models import Q
from .serializers import PlayerSerializer
from .models import Player

class RegisterPlayerView(generics.CreateAPIView):
    queryset = Player.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlayerSerializer

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        login_input = request.data.get('username') # can be email or username
        password = request.data.get('password')
        
        # Try to find the user by username OR email
        try:
            user_obj = Player.objects.get(Q(username=login_input) | Q(email=login_input))
            username = user_obj.username
        except Player.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=username, password=password)
        
        if user:
            serializer = PlayerSerializer(user)
            return Response({
                'user': serializer.data,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

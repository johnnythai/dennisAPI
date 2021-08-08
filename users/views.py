from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, generics

from .serializer import UserSerializer, GroupSerializer
from django.contrib.auth.models import User, Group

class CreateUser(APIView):
    """
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, format='json'):
        """
        POST request to create and save new users.
        """
        context = {
            'request': request
        }
        serializer = UserSerializer(data=request.data, context=context)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data)
        return Response(serializer.errors)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
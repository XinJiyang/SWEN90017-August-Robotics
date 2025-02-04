import json, jwt, time
from django.http import JsonResponse
from AccountManagement.models import Account
from django.contrib.auth.hashers import make_password, check_password
from psycopg2.errors import DataError, StringDataRightTruncation
from .models import Account

from .serializers import AccountSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView 
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import RoleBasedPermission


def generate_token(username) -> str:
    """generate token based on the user's name and role"""
    payload = {'username': username, 'exp': int(time.time()) + TOKEN_EXPIRE_TIME}
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return token


from django.contrib.auth.models import Group

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Assign user to a group based on their privilege
        group_name = user.privilege  
        try:
            user_group = Group.objects.get(name=group_name)
            user.groups.add(user_group)
            user.save()
        except Group.DoesNotExist:
            return Response({'error': f'Group {group_name} does not exist.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': 'Account created successfully.',
                         'account': {'username': user.username, 'privilege': user.privilege}},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    permission_classes_by_action = {'create': [permissions.AllowAny],
                                    'retrieve': [RoleBasedPermission],
                                    'update': [RoleBasedPermission],
                                    'delete': [RoleBasedPermission]}

    
    def get(self, request, username, *args, **kwargs):
        try:
            user = Account.objects.get(username=username)
            serializer = AccountSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, username, *args, **kwargs):
        try:
            user = Account.objects.get(username=username)
            if request.user != user:
                return Response({'error': 'You are not authorized to update this user'},
                                status=status.HTTP_403_FORBIDDEN)

            serializer = AccountSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': 'User updated successfully', 'user': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Account.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, username, *args, **kwargs):
        try:
            user = Account.objects.get(username=username)
            if request.user != user and not request.user.is_staff:
                return Response({'error': 'You are not authorized to delete this user'},
                                status=status.HTTP_403_FORBIDDEN)

            user.delete()
            return Response({'success': 'User deleted successfully'}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def get_permissions(self):
        try:
            if self.request.method.lower() == 'post':
                self.action = 'create'
            elif self.request.method.lower() == 'get':
                self.action = 'retrieve'
            elif self.request.method.lower() == 'put':
                self.action = 'update'
            elif self.request.method.lower() == 'delete':
                self.action = 'delete'
                
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set, return default permission_classes
            return [permission() for permission in self.permission_classes]

from django.shortcuts import render
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import permissions,viewsets,status,response
from .models import *
from django.contrib.auth import login
from .serializers import *
from rest_framework import filters
from rest_framework.exceptions import ValidationError

# Create your views here.
# custom permission
class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    

    def has_object_permission(self, request, view, obj):
        return bool(obj == request.user)

class LoginView(KnoxLoginView):
    """
    API endpoint that for login overides post method of KnoxloginView.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        output_list =  super(LoginView, self).post(request, format=None)
        output_list.data["user"]["id"] = user.id
        output_list.data["user"]["email"] = user.email
        return response.Response({"data":output_list.data})
    # def post(self, request, format=None):
    #     serializer = AuthTokenSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     login(request, user)
    #     return super(LoginView, self).post(request, format=None)



class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited. overides destroy method 
    to set user as inactive instead of deleteimg user ,acessible only to owner and admin 
    users staff() or superuser and update can only be done by owner
    """
    queryset = CustomUser.objects.filter(is_active=True).order_by('-date_joined')
    # serializer_class = CustomUserSerializer
    search_fields = ['first_name','last_name','email','id','username']
    filter_backends = (filters.SearchFilter,)
    
    permission_classes_by_action = {'create': [permissions.AllowAny],
                                    'list': [permissions.AllowAny],
                                    'retrieve': [permissions.AllowAny],
                                    'update': [IsOwner],
                                    'destroy': [permissions.IsAdminUser|IsOwner],
                                    'partial_update': [IsOwner]}

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action in ['change_password']:
            return ChangePasswordSerializer
        return CustomUserSerializer

    

    # def get_permissions(self):
    #     if self.request.method == 'delete' or 'patch' or 'put':
    #     # if self.request.method == 'get' or 'post':
    #         self.permission_classes = (IsOwner|permissions.IsAdminUser,)
    #     # else:
    #     #     self.permission_classes = (permissions.AllowAny,)
           
    #     # if self.request.method == 'POST' or 'GET':
    #     #     self.permission_classes = (permissions.AllowAny,)
 
    #     return super().get_permissions()
    #issue with authentication cod isOwner

    # def get_queryset(self):
    #     try:
    #         user = self.request.user
    #         if user.is_staff and user.is_superuser:
    #             return CustomUser.objects.all().order_by('-created_on')     
    #         else:
    #             return CustomUser.objects.filter(id=user).order_by('-created_on')
    #     except:
    #         raise ValidationError(detail='Improper request')

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user or request.user.is_superuser:
            user.is_active = False
            user.save()
            return response.Response(data={'msg':'done'},status=status.HTTP_200_OK)
        else:
            raise ValidationError(detail='not allowed',code=status.HTTP_401_UNAUTHORIZED)

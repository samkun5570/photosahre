from django.shortcuts import render
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import permissions,viewsets,status,response
from .models import *
from django.contrib.auth import login
from .serializers import *
from rest_framework import filters

# Create your views here.
# custom permission
class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj == request.user

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
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = CustomUserSerializer
    search_fields = ['first_name','last_name','email','id','username']
    filter_backends = (filters.SearchFilter,)
    def get_permissions(self):
        if self.request.method == 'POST' or 'GET':
            self.permission_classes = (permissions.AllowAny,)
        elif self.request.method ==  'PATCH' or 'PUT':
            self.permission_classes = (permissions.IsAuthenticated and IsOwner)
        elif self.request.method == 'DELETE':
            self.permission_classes = (permissions.IsAuthenticated and IsOwner)
        return super(CustomUserViewSet, self).get_permissions()
    #issue with authentication cod isOwner

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()

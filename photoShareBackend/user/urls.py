from django.urls import include, path
from rest_framework import routers
from .views import *
from rest_framework.routers import DefaultRouter



#create router for user viewset acessebile using "/users/ path"
router = DefaultRouter()
router.register(r'users', CustomUserViewSet,basename='users')


urlpatterns = [
    path('', include(router.urls)),
]

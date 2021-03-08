from django.urls import include, path
from rest_framework import routers
from .views import *
from rest_framework.routers import DefaultRouter



#create router for user viewset acessebile using "/users/ path"
router = DefaultRouter()
router.register(r'comment', CommentViewSet,basename='comment')
router.register(r'like', LikeViewSet,basename='comment')
router.register(r'post', PostViewSet,basename='comment')
router.register(r'following', FollowingViewSet,basename='comment')



urlpatterns = [
    path('', include(router.urls)),
    path('userFollowing',GetUserFollowing.as_view()),
    path('userFollower',GetUserFollower.as_view()),
]

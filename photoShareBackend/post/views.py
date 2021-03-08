from django.shortcuts import render
from rest_framework import viewsets,permissions
from rest_framework.exceptions import ValidationError
from .models import *
from .serializers import *
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.decorators import action


# Create your views here.


"""custom permissions"""

class IsPostOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user 

class IsCommentOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj.comment_author == request.user 

class IsLikeOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj.like_author == request.user

class IsFollowingOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj.follower == request.user


#custom permission class for readonly
class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


"""views"""


#viewset for comment related function use search query to get specfic comment related to 
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer  
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ('comment_post','comment_author')
    # filterset_fields =[]
    # ordering =('-created_on',)
    search_fields = ('comment_text',)
    queryset =  Comment.objects.all().order_by('-created_on')    

    def get_permissions(self):
        if self.request.method == 'POST' or 'GET':
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.request.method ==  'PATCH' or 'UPDATE':
            self.permission_classes = (IsCommentOwner,)
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsCommentOwner|permissions.IsAdminUser]
        return super(CommentViewSet, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(comment_author=self.request.user)

#viewset for post related function to acess list of post of user by 
class PostViewSet(viewsets.ModelViewSet):  
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields =('author','location')
    # filterset_fields =[]
    # ordering =('-created_on',)
    search_fields =('caption',)
    serializer_class = PostSerializer
    queryset =  Post.objects.all().order_by('-created_on')    

    def get_permissions(self):
        if self.request.method == 'POST' or 'GET':
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.request.method ==  'PATCH' or 'PUT':
            self.permission_classes = (IsPostOwner,)
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsPostOwner|permissions.IsAdminUser]
        return super(PostViewSet, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_queryset(self):
    #     try:
    #         user = self.request.user
    #         if user.is_staff and user.is_superuser:
    #             return Post.objects.all().order_by('-created_on')     
    #         else:
    #             return Post.objects.filter(author=user).order_by('-created_on')
    #     except:
    #         raise ValidationError(detail='Imporpoer request')

#viewset for like related functionalities to like a post pass the id of the post in like_post filed and to delete like with id of post in like_post field and id of user in like_author field
#likes can be searched using 'like_post=','like_author='
class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields =('like_post','like_author')
    # filterset_fields =['like_post','like_author']
    # ordering =('-created_on',)
    # search_fields =('caption',)
    serializer_class = LikeSerializer
    queryset = Like.objects.all().order_by('-created_on')  

    def get_permissions(self):
        if self.request.method == 'POST' or 'GET':
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.request.method ==  'PATCH' or 'PUT' or 'DELETE' :
            self.permission_classes = (IsLikeOwner,)
        return super(LikeViewSet, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(like_author=self.request.user)

    # def get_queryset(self):
    #     try:
    #         user = self.request.user
    #         if user.is_staff and user.is_superuser:
    #             return Like.objects.all().order_by('-created_on')     
    #         else:
    #             return Like.objects.filter(author=user).order_by('-created_on')
    #     except:
    #         raise ValidationError(detail='Imporpoer request')

#viewset for follow  functionalities ,to follow a user pass the id of the user in following filed and to unfollow delete Following 
#following can be searched using 'follower=','following='

class FollowingViewSet(viewsets.ModelViewSet):
    serializer_class = FollowingSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields =('follower','following')
    queryset = Following.objects.all()

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)
    
    def get_permissions(self):
        if self.request.method == 'POST' or 'GET':
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.request.method ==  'PATCH' or 'PUT' or 'DELETE':
            self.permission_classes = (IsFollowingOwner,)
        return super(FollowingViewSet, self).get_permissions()

 
 # get list of following 
class GetUserFollowing(generics.ListAPIView):
    serializer_class = FollowingCustomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Following.objects.filter(follower=self.request.user).distinct().order_by('-created_on')

 # get list of follower 
class GetUserFollower(generics.ListAPIView):
    serializer_class = FollowerCustomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Following.objects.filter(following=self.request.user).distinct().order_by('-created_on')
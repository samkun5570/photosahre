from .models import  *
from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin

class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Following
        fields = '__all__'
        read_only_fields = ('created_on','last_modified')
        depth = 1

class FollowingCustomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Following
        fields = ['id','following']
        depth = 1
   

class FollowerCustomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Following
        fields = ['id','follower']
        depth = 1
  

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ('created_on','last_modified')
        depth = 1

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created_on','last_modified')
        depth = 1

class PostSerializer(QueryFieldsMixin,serializers.ModelSerializer):
    number_of_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','author','photo','location','caption','number_of_likes']
        read_only_fields = ('created_on','last_modified','number_of_likes')
        depth = 1

    def get_number_of_likes(self, obj):
        return Like.objects.filter(like_post=obj).count()


        

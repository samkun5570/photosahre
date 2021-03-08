from .models import  *
from rest_framework import serializers

class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Following
        fields = '__all__'
        read_only_fields = ('created_on','last_modified')

class FollowingCustomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Following
        fields = ['following']
   

class FollowerCustomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Following
        fields = ['follower']
  

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ('created_on','last_modified')

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created_on','last_modified')

class PostSerializer(serializers.ModelSerializer):
    number_of_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['author','photo','location','caption','number_of_likes']
        read_only_fields = ('created_on','last_modified','number_of_likes')

    def get_number_of_likes(self, obj):
        return Like.objects.filter(like_post=obj).count()


        

from .models import  *
from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from user.serializers import CustomUserSerializer

class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Following
        fields = '__all__'
        read_only_fields = ('created_on','last_modified')
        depth = 1

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['follower'] = CustomUserSerializer(instance.follower).data
    #     rep['following'] = CustomUserSerializer(instance.following).data
    #     return rep
         

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
    thumbnail = serializers.ImageField(source='photo_thumbnail',read_only=True)

    class Meta:
        model = Post
        fields = ['id','author','photo','location','caption','number_of_likes','thumbnail']
        read_only_fields = ('created_on','last_modified','number_of_likes')
        depth = 1

    def get_number_of_likes(self, obj):
        return Like.objects.filter(like_post=obj).count()


        

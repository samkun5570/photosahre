from rest_framework import serializers
from django.contrib.auth import get_user_model
from post.models import Post



"""Serializer for viewing a user complete detail except follower,follwing and post details"""
class CustomUserSerializer(serializers.ModelSerializer):

    number_of_posts = serializers.SerializerMethodField()
    number_of_following = serializers.SerializerMethodField()
    number_of_followers = serializers.SerializerMethodField()
    thumbnail = serializers.ImageField(source='avatar_thumbnail',read_only=True)
   
    class Meta:
        model = get_user_model()
        fields = ['id','first_name','last_name','email','password','is_staff','is_superuser','bio','avatar','username','is_active','thumbnail',
        'last_login','date_joined','number_of_posts','number_of_following','number_of_followers']
        read_only_fields = ('id','is_staff','is_superuser','is_active','last_login','date_joined','number_of_posts','thumbnail','number_of_following','number_of_followers')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_number_of_following(self, obj):
        return obj.followings.all().count()

    def get_number_of_followers(self, obj):
        return obj.followers.all().count()
    
    def get_number_of_posts(self, obj):
        return Post.objects.filter(author=obj).count()

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(CustomUserSerializer, self).update(instance, validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()

    def update(self, instance, validated_data):
        password_valid = instance.check_password(validated_data.get('old_password'))
        if not password_valid:
            error = {'error': "Wrong password"}
            raise serializers.ValidationError(
                error
            )

        instance.set_password(validated_data.get('new_password'))
        instance.save()

        return instance



from django.db import models
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from rest_framework import serializers


# Create your models here.
class AbstractBaseModel(models.Model):
    """
        Captures BaseContent as created On and modified On and active field.
        common field accessed for the following classes.
    """

    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
   
  
    class Meta:
        abstract = True

    def __str__(self):
        return self.id

class CaseInsensetiveModelbackend(ModelBackend):
    def authenticate(self,request,username=None,password=None,**kwargs):
        UserModel = get_user_model()
        if username is None:
            username =kwargs.get(UserModel.USERNAME_FIELD)
        try:
            case_insensetive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            user = UserModel._default_manager.get(**{case_insensetive_username_field:username})
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
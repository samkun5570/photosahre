from django.db import models
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


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
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField,ImageSpecField
from imagekit.processors import ResizeToFit,ResizeToFill

# Create your models here.

# gender choices
# class GENDER_CHOICES(models.TextChoices):
#     Male = u'M', 'Male'
#     Female = u'F', 'Female'
#     Other = u'O', 'Other'

#custom user inhereting from abstract user to add additional fields
class CustomUser(AbstractUser):
    # gender = models.CharField( _('Gender'), max_length=10, choices=GENDER_CHOICES.choices, null=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/%y/%m/%d', default='avatar.png')
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(75, 75)],
                                      format='JPEG',
                                      options={'quality': 60}
                                      )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-date_joined']

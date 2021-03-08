from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from photoShareBackend.Base import AbstractBaseModel
from imagekit.models import ProcessedImageField,ImageSpecField
from imagekit.processors import ResizeToFit,ResizeToFill
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
#post model inhereting from abstractbasemodel
class Post(AbstractBaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_posts')
    photo = models.ImageField(upload_to='photo/%y/%m/%d', null =False) 
    # photo_thumbnail = ImageSpecField(source='photo',
    #                                   processors=[ResizeToFill(150, 150)],
    #                                   format='JPEG',
    #                                   options={'quality': 60}
    #                                   )
    location  =  models.TextField(_('Post location '), max_length=30, blank=True,null=True)   
    caption  = models.TextField(_('Post caption '), max_length=430, blank=True,null=True)   

    class Meta:
        ordering = ['-created_on']
  
    def __str__(self):
        return f'{self.author}-{self.created_on}-{self.id}'

#Commemt relationship model  inhereting from abstractbasemodel
class Comment(AbstractBaseModel):
    comment_post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='post_comments')
    comment_author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='user_comments')
    comment_text = models.CharField(max_length=100)
    

    class Meta:
       ordering = ['-created_on']

    def __str__(self):
        return f'{self.comment_author} comments {self.comment_post} on {self.created_on}'


#Like relationship used instead of many to many field  inhereting from abstractbasemodel
class Like(AbstractBaseModel):
    like_post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_likes')
    like_author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='author_likes')

    class Meta:
        unique_together = (("like_post", "like_author"),)
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.like_author} likes {self.like_post} on {self.created_on}'

#follower and folowing relationship used instead of many to many field  inhereting from abstractbasemodel
class Following(AbstractBaseModel):

    follower = models.ForeignKey(User, related_name="followings", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower','following'],  name="unique_followers")
        ]


        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.follower} follows {self.following}"
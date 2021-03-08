from django.contrib import admin
from .models import  *

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
#in admin user can follow user further developemt is needed to solve the issue
admin.site.register(Following)

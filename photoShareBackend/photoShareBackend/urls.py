"""photoShareBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin,auth
from django.urls import path,include
from django.conf.urls import url
from knox import views as knox_views
from user.views import LoginView
from rest_framework import permissions
from django.conf import settings
# from rest_framework.schemas import get_schema_view
from django.conf.urls.static import static

from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls

# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

schema_view = get_swagger_view(title='test photoshare API')

# schema_view = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version='v1',
#       description="Test description",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=[permissions.AllowAny],
# )

urlpatterns = [
    # url('',schema_view),
    # url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('openapi', get_schema_view(
    #     title="Your Project",
    #     description="API for all things …"
    # ), name='openapi-schema'),
    path('docs/', schema_view, name="docs"),
    path('api-docs/', include_docs_urls(title='photoshare API')),
    path('admin/', admin.site.urls),
    path('api-login/', LoginView.as_view(), name='knox_login'),
    path('api-logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api-logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-user/',include('user.urls')),
    path('api-post/',include('post.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

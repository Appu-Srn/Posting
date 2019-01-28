
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/auth/login/$', obtain_jwt_token, name='api_login'),
    url('^api/posting/', include('posting.api.urls'))
]



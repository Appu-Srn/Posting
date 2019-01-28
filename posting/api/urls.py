from .views import *
from django.conf.urls import url


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', BlogPostApiView.as_view(), name='post_listcreate'),
    url(r'^(?P<pk>\d+)/$', BlogPostRudView.as_view(), name='post_rud')

]
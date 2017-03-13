from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^(?P<AgencyDetail_id>[0-9]+)/$', views.awblist, name='awblist')
]

from django.conf.urls import url, include, static

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^agencies/$', views.AgencyListView.as_view(), name='Agencies'),
    # url(r'^agencies/(?P<pk>\d+)/$', views.AgencyDetailView.as_view(), name='agency-detail'),
]

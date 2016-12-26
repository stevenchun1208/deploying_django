from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.pokes, name='pokes'),
    url(r'^poked/(?P<id>\d+)$', views.poked, name = 'poked'),
    url(r'^logout$', views.logout, name='logout')
]

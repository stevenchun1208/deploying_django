from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^processreg$', views.processreg, name = "registration"),
    url(r'^processlog$', views.processlog, name = 'login')
]

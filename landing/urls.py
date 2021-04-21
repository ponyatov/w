from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='landing'),
    # url(r'^$', views.form_view, name='form_view')
]

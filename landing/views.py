import config

from django.http import Http404, HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
# from django.urls import resolve

from app.models import *

# Create your views here.

def index(request):
    index_html = get_template('index.html')
    apps = App.objects.all()
    app = apps.get(name=__package__)
    c = {'apps': apps, 'app': app,
         'MODULE': config.MODULE, 'package': __package__}
    return HttpResponse(index_html.render(c))

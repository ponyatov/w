import config
import datetime as dt

from django.http import Http404, HttpResponse
# from django.template import Template, Context
from django.template.loader import get_template

ct_json = 'text/json; charset=utf8'

# all_html = get_template('all.html')
# index_html = get_template('index.html')

def index(request):
    index_html = get_template('index.html')
    c = {'MODULE': config.MODULE, 'package': __package__}
    return HttpResponse(index_html.render(c))


# from django.core import serializer
import json

def localtime(request):
    now = dt.datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M:%S')
    ret = {'date': date, 'time': time, 'iso': f'{date} {time}'}
    # json = serializers.serialize('json',ret)
    # return HttpResponse(json)
    return HttpResponse(json.dumps(ret), content_type=ct_json)


def dynamic(request, pa, ram):
    return HttpResponse(f'{request} {pa},{ram}', content_type=ct_json)

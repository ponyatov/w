import datetime as dt

from django.http import HttpResponse

ct_json = 'text/json; charset=utf8'

def hello(request):
    return HttpResponse("Hello world")


# from django.core import serializers
import json

def localtime(request):
    now = dt.datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M:%S')
    ret = {'date': date, 'time': time, 'iso': f'{date} {time}'}
    # json = serializers.serialize('json',ret)
    # return HttpResponse(json)
    return HttpResponse(json.dumps(ret),
                        content_type=ct_json)


def dynamic(request):
    return HttpResponse(f'{request}', content_type=ct_json)

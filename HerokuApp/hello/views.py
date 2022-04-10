from django.shortcuts import render
from django.http import HttpResponse

import requests

# Create your views here.
def index(request):
    r = requests.get('https://httpbin.org/status/418')
    print(r.text)
    # return HttpResponse('Hello from Python!')
    return HttpResponse(f'<pre>{r.text}</pre>')

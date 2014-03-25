from django.shortcuts import render

from django.http import HttpResponse, HttpRequest
from trademarks.models import Word
from trademarks.algorithm import *

def home(request):
    context = {'forsearch': ''}
    return render(request, 'index.html', context)

def search(request):
    input = request.GET['findme']
    p = DoubleMetaphon(input).transcription
    data = dict()
    final = dict()
    langs = list()
    if p != '':
        raw = list(Word.objects.filter(ipa__contains=p))
        for item in raw: 
            if item.lang not in data:
                langs.append(item.lang)
                data[item.lang] = list()
                for i in [0,1,2]:
                    data[item.lang].append(list())
            if item.ipa == p:
                data[item.lang][0].append(item)
            elif item.ipa.startswith(p):
                data[item.lang][1].append(item)
            else:
                data[item.lang][2].append(item)
        for lang in langs:
            final[lang] = data[lang][1] + data[lang][1] + data[lang][2]
    context = {'array' : final, 'forsearch': input, 'langs' : langs}
    return render(request, 'search.html', context)
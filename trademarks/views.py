from django.shortcuts import render

from django.http import HttpResponse, HttpRequest
from trademarks.models import Word
from trademarks.algorithm import *
import random

def home(request):
    context = {'forsearch': ''}
    return render(request, 'index.html', context)

def search(request):
    input = request.GET['findme']
    try:
        sorting = request.GET['matchsort']
    except:
        sorting = '0'
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
                data[item.lang][0].append([item, random.randint(0,100)])
            elif item.ipa.startswith(p):
                data[item.lang][1].append([item, random.randint(0,100)])
            else:
                data[item.lang][2].append([item, random.randint(0,100)])
        for lang in langs:
            if sorting != '0':
                for i in [0,1,2]:
                    data[lang][i].sort(key=lambda l:int(l[1]), reverse = True)
            final[lang] = data[lang][0] + data[lang][1] + data[lang][2]
    context = {'array' : final, 'forsearch': input, 'langs' : langs, 'debug' : p + sorting, 'sort' : sorting}
    return render(request, 'search.html', context)

def search_sortbymatch(request, array):

    return render(request, 'index.html', {})
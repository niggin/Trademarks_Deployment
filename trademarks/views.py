from django.shortcuts import render

from django.http import HttpResponse, HttpRequest
from django.utils import simplejson
from django.core import serializers
from trademarks.models import Word
from trademarks.algorithm import *
from trademarks.metric import metric

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
    
    final = dict()
    langs = list()
    if p != '':
        raw = list(Word.objects.filter(ipa__contains=p))
        if sorting == '0':
            data = dict()
            for item in raw:
                if item.lang not in data:
                    langs.append(item.lang)
                    data[item.lang] = list()
                    for i in range(3):
                        data[item.lang].append(list())
                if item.ipa == p:
                    data[item.lang][0].append([item, metric(p,item.ipa)])
                elif item.ipa.startswith(p):
                    data[item.lang][1].append([item, metric(p,item.ipa)])
                else:
                    data[item.lang][2].append([item, metric(p,item.ipa)])
                for lang in langs:
                    for array in data[lang]:
                        array.sort(key=lambda l:int(l[1]), reverse = True)
                    final[lang] = data[lang][0] + data[lang][1] + data[lang][2]
        else:
            langs = ['all']
            data = [[item, metric(p,item.ipa)] for item in raw]
            data.sort(key = lambda l:l[1], reverse = True)
            final = {'all': data}
    context = {'array' : final, 'forsearch': input, 'langs' : langs, 'debug' : p + sorting, 'sort' : sorting}
    return render(request, 'search.html', context)

def search_sortbymatch(request):
    input = request.GET['findme']
    try:
        sorting = request.GET['matchsort']
    except:
        sorting = '0'
    p = DoubleMetaphon(input).transcription
    
    final = dict()
    langs = list()
    if p != '':
        if len(p)<2:
            raw = list(Word.objects.filter(ipa=p))
        else:
            raw = list(Word.objects.filter(ipa__contains=p))
        if sorting == '0':
            data = dict()
            for item in raw:
                if item.lang not in data:
                    langs.append(item.lang)
                    data[item.lang] = list()
                    for i in range(3):
                        data[item.lang].append(list())
                if item.ipa == p:
                    data[item.lang][0].append([item.serialize(), metric(p,item.ipa)])
                elif item.ipa.startswith(p):
                    data[item.lang][1].append([item.serialize(), metric(p,item.ipa)])
                else:
                    data[item.lang][2].append([item.serialize(), metric(p,item.ipa)])
                for lang in langs:
                    for array in data[lang]:
                        array.sort(key=lambda l:int(l[1]), reverse = True)
                    final[lang] = data[lang][0] + data[lang][1] + data[lang][2]
        else:
            langs = ['all']
            data = [[item, metric(p,item.ipa)] for item in raw]
            data.sort(key = lambda l:l[1], reverse = True)
            final = {'all': data}
    #context = {'array' : final, 'forsearch': input, 'langs' : langs, 'debug' : p + sorting, 'sort' : sorting}
    context = {'forsearch': input, 'sort' : sorting, 'langs': langs,
               'debug': p + sorting, 'array': final}
    json = simplejson.dumps(context)
    return HttpResponse(json, mimetype='application/json')
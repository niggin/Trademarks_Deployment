from django.shortcuts import render

from django.http import HttpResponse, HttpRequest
from django.utils import simplejson
from django.core import serializers
from trademarks.models import Word
from trademarks.algorithm import *
from trademarks.metric import metric
from django.core.cache import cache
import sys, json

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
    lang_skip = request.GET['lang']
    p = DoubleMetaphon(input).transcription
    
    langs = list()
    position = dict()
    fromcache = cache.get(str(request.user.id) + "findme")
    if not fromcache or input + lang_skip != fromcache:
        final = dict()
        if p != '':
            if len(p)<1:
                raw = list(Word.objects.filter(ipa=p))
            else:
                raw = list(Word.objects.filter(ipa__contains=p))
            for item in raw:
                if item.lang not in final:
                    langs.append(item.lang)
                    final[item.lang] = list()
                if item.lang == lang_skip:
                    item.meaning = ''
                final[item.lang].append([item.serialize(), metric(p,item.ipa)])
            for lang in langs:
                final[lang].sort(key=lambda l:int(l[1]), reverse = True)
                position[lang] = 10
        cache.set(str(request.user.id) + "array", final)
        cache.set(str(request.user.id) + "findme", input + lang_skip)
        cache.set(str(request.user.id) + "position", position)
        cache.set(str(request.user.id) + "langs", langs)
    else:
        final = cache.get(str(request.user.id) + "array")
        position = cache.get(str(request.user.id) + "position")
        langs = cache.get(str(request.user.id) + "langs")
    output = dict()
    for i in range(len(langs)):
        output[langs[i]] = final[langs[i]][position[langs[i]]-10:position[langs[i]]]
    context = {'forsearch': input, 'langs': langs,
               'debug': p, 'array': output}
    json_out = json.dumps(context)
    return HttpResponse(json_out, content_type='application/json')

def load_more(request):
    final = cache.get(str(request.user.id) + "array")
    langs = cache.get(str(request.user.id) + "langs")
    position = cache.get(str(request.user.id) + "position")
    update_lang = request.GET['lang']
    output = dict()
    position[update_lang] += 10
    output[update_lang] = final[update_lang][position[update_lang]-10:position[update_lang]]
    context = {'array': output}
    json_out = json.dumps(context)
    return HttpResponse(json_out, content_type='application/json')
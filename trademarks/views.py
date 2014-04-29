# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.http import HttpResponse, HttpRequest
from django.utils import simplejson
from django.core import serializers
from trademarks.models import Word
from trademarks.algorithm import *
from trademarks.metric import *
from trademarks.analyzer import *
from django.core.cache import cache
import sys, json

def home(request):
    context = {'forsearch': ''}
    return render(request, 'index.html', context)

"""def search(request):
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
    return render(request, 'search.html', context)"""

def search(request):
    input = request.GET['findme']
    lang_skip = request.GET['translate']
    shown_langs = request.GET.getlist('langs[]')
    print >>sys.stderr, shown_langs
    metaphon = DoubleMetaphon()
    p = metaphon.getTranscription(unicode(input))

    p_fullipa = analyzer(input, p)
    
    langs = list()
    position = dict()
    fromcache = cache.get(str(request.user.id) + "findme")
    if not fromcache or input + lang_skip + ''.join(shown_langs) != fromcache:
        final = dict()
        if p != '':
            if len(p)<1:
                raw = list(Word.objects.filter(ipa=p, lang__in=shown_langs))
            else:
                raw = list(Word.objects.filter(ipa__contains=p, lang__in=shown_langs))
            print >>sys.stderr, "fetched", len(raw)
            for item in shown_langs:
                final[item] = list()
            for item in raw:
                if lang_skip == "en":
                    item.meaning = item.meaning_eng
                if item.lang == lang_skip:
                    item.meaning = ''
                if item.fullipa == "":
                    #print >>sys.stderr, item.word
                    item_fullipa = analyzer(item.word,item.ipa)
                else:
                    item_fullipa = item.fullipa
                score = metricOfTranscriptions(p_fullipa, item_fullipa)
                final[item.lang].append([item.serialize(), (1 - score)*100])
            #print >>sys.stderr, "metric executed"
            for lang in shown_langs:
                if len(final[lang])>0:
                    #final[lang].sort(key=lambda l:int(l[1]), reverse = True)
                    final[lang] = sorted(final[lang], key=lambda l:l[1], reverse = True)
                    position[lang] = min(10,len(final[lang]))
                else:
                    final.pop(lang)
            print >>sys.stderr, "sorted"
        cache.set(input + lang_skip + ''.join(shown_langs), final)
        cache.set(str(request.user.id) + "findme", input + lang_skip + ''.join(shown_langs))
        cache.set(str(request.user.id) + "position", position)
    else:
        final = cache.get(fromcache)
        position = cache.get(str(request.user.id) + "position")
    output = dict()
    print >>sys.stderr, final.keys(), shown_langs, position
 
    for item in final:
        output[item] = final[item][max(0,position[item]-10):position[item]]
    context = {'forsearch': input, 'langs': final.keys(),
               'debug': p, 'array': output, 'hide_morebutton': {item: position[item] == len(final[item]) for item in final} }
    json_out = json.dumps(context)
    return HttpResponse(json_out, content_type='application/json')

def load_more(request):
    final = cache.get(cache.get(str(request.user.id) + "findme"))
    langs = final.keys()
    position = cache.get(str(request.user.id) + "position")
    update_lang = request.GET['lang']
    output = dict()
    delta = 10
    if position[update_lang] + 10 < len(final[update_lang]):
        position[update_lang] += 10
    elif position[update_lang] < len(final[update_lang]):
        delta = len(final[update_lang]) - position[update_lang]
        position[update_lang] = len(final[update_lang])
    else:
        delta = 0
    output[update_lang] = final[update_lang][position[update_lang]-delta:position[update_lang]]
    context = {'array': output, 'hide_morebutton': {item: position[item] == len(final[item]) for item in final} }
    cache.set(str(request.user.id) + "position", position)
    json_out = json.dumps(context)
    return HttpResponse(json_out, content_type='application/json')

def metric(a,b):
    import random
    return random.randint(0,100)
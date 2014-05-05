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
import sys, json, time, math


def home(request):
    context = {'forsearch': ''}
    return render(request, 'index.html', context)

def search(request):
    sec = time.time()
    input = request.GET['findme']
    lang_skip = request.GET['translate']
    shown_langs = request.GET.getlist('langs[]')
    print >>sys.stderr, shown_langs
    metaphon = DoubleMetaphon()
    p = metaphon.getTranscription(unicode(input))

    p_fullipa = Word.objects.filter(word__exact=input, fullipa__isnull=False)
    if p_fullipa:
        p_fullipa = p_fullipa[0].fullipa
    else:
        p_fullipa = analyzer(input, p)
    
    langs = list()
    position = dict()
    fromcache = cache.get(str(request.user.id) + "findme")
    if not fromcache or input + lang_skip + ''.join(shown_langs) != fromcache:
        print >>sys.stderr, "not from cache"
        final = dict()
        if p != '':
            #raw = list(Word.objects.raw('SELECT * FROM trademarks_word WHERE ("' 
            #                             + p + '" LIKE CONCAT("%%",ipa,"%%") OR ipa LIKE "%%' 
            #                             + p + '%%") AND lang IN (' + ", ".join('"%s"'% arg for arg in shown_langs) + ')'))
            raw = list(Word.objects.filter(ipa__contains=p,lang__in=shown_langs))
            print >>sys.stderr, "fetched"
            for item in shown_langs:
                final[item] = list()
            for item in raw:
                if lang_skip == "en":
                    item.meaning = item.meaning_eng
                if item.lang == lang_skip:
                    item.meaning = ''
                if item.fullipa == None:
                    item_fullipa = analyzer(item.word,item.ipa)
                else:
                    item_fullipa = item.fullipa
                score = metricOfTranscriptions(p_fullipa, item_fullipa)
                final[item.lang].append([item.serialize(), func(score)])#math.exp(-score*gamma) * 100])
            print >>sys.stderr, "metric executed"
            for lang in shown_langs:
                if len(final[lang])>0:
                    final[lang] = sorted(final[lang], key=lambda l:l[1], reverse = True)
                    position[lang] = min(10,len(final[lang]))
                else:
                    final.pop(lang)
            print >>sys.stderr, "sorted"
        cache.set(input + lang_skip + ''.join(shown_langs), final)
        cache.set(str(request.user.id) + "findme", input + lang_skip + ''.join(shown_langs))
        cache.set(str(request.user.id) + "position", position)
    else:
        print >>sys.stderr, "from cache"
        final = cache.get(fromcache)
        for lang in final:
            position[lang] = min(10,len(final[lang]))
        cache.set(str(request.user.id) + "position", position)
        #position = cache.get(str(request.user.id) + "position")
    output = dict()
    print >>sys.stderr, final.keys(), shown_langs, position
 
    for item in final:
        output[item] = final[item][max(0,position[item]-10):position[item]]
    context = {'forsearch': input, 'langs': final.keys(),
               'debug': p, 'array': output, 'hide_morebutton': {item: position[item] == len(final[item]) for item in final} }
    json_out = json.dumps(context)
    print time.time() - sec
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

def func(score):

    return 100 * (1 - score)
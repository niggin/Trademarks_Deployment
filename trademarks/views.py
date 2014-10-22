# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.mail import send_mail

from django.http import HttpResponse, HttpRequest
from django.utils import simplejson
from django.core import serializers
from trademarks.models import Word, History
from trademarks.algorithm import *
from trademarks.metric import *
from trademarks.analyzer import *
from django.core.cache import cache
from trademarks.settings import DEBUG
#from trademarks.settings import custom_DEBUG
import sys, json, time, math

cache_time = 600


def home(request):
    if not request.session.get('has_session'):
        request.session['has_session'] = True
    context = {'forsearch': '', 'DEBUG': DEBUG}
    return render(request, 'index.html', context)

def search(request):
    id = request.session.session_key
    sec = time.time()
    input = request.GET['findme']
    lang_skip = request.GET['translate']
    shown_langs = request.GET.getlist('langs[]')
    #print (shown_langs,file=sys.stderr)
    metaphon = DoubleMetaphon()
    p = metaphon.getTranscription(input)

    print >>sys.stderr, request.GET

    #History
    history = History.objects.filter(word=input)
    if(history.count()):
        history = history[0]
        history.requests += 1
    else:
        history = History(word=input, requests=1)
    history.save()

    p_fullipa = Word.objects.filter(word__exact=input, fullipa__isnull=False)
    if p_fullipa:
        p_fullipa = p_fullipa[0].fullipa
    else:
        p_fullipa = analyzer(input, p)
    
    langs = list()
    position = dict()
    fromcache = cache.get(id + "findme")
    session_request = input + lang_skip + ''.join(shown_langs)
    if 1:#if not fromcache or input + lang_skip + ''.join(shown_langs) != fromcache:
        #print ("not from cache",file=sys.stderr)
        final = dict()
        if p != '':
            #raw = list(Word.objects.raw('SELECT * FROM trademarks_word WHERE ("' 
            #                             + p + '" LIKE CONCAT("%%",ipa,"%%") OR ipa LIKE "%%' 
            #                             + p + '%%") AND lang IN (' + ", ".join('"%s"'% arg for arg in shown_langs) + ')'))
            if shown_langs[0] == "all":
                raw = list(Word.objects.filter(ipa__contains=p,lang__in=["ru", "en"]))
            else:
                raw = list(Word.objects.filter(ipa__contains=p,lang__in=shown_langs))
            #print ("fetched",file=sys.stderr)
            for item in shown_langs:
                final[item] = list()
            for item in raw:
                if lang_skip == "en":
                    item.meaning = item.meaning_eng
                if item.lang == lang_skip and shown_langs[0] != "all":
                    item.meaning = ''#item.word
                elif item.lang == lang_skip:
                    item.meaning = item.word
                if item.fullipa:
                    item_fullipa = item.fullipa
                else:
                    item_fullipa = analyzer(item.word,item.ipa)
                score = metricOfTranscriptions(p_fullipa, item_fullipa)
                if shown_langs[0] == "all":
                    final["all"].append([item.serialize(), func(score)])
                else:
                    final[item.lang].append([item.serialize(), func(score)])#math.exp(-score*gamma) * 100])
            #print ("metric executed",file=sys.stderr)
            for lang in shown_langs:
                if len(final[lang])>0:
                    final[lang] = sorted(final[lang], key=lambda l:l[1], reverse = True)[:1000]
                    position[lang] = min(10,len(final[lang]))
                else:
                    final.pop(lang)
            #print ("sorted",file=sys.stderr)
        res = cache.set(id, final, cache_time)
        cache.set(id + "findme", input + lang_skip + ''.join(shown_langs), cache_time)
        cache.set(id + "position", position, cache_time)
    """else:
        print >>sys.stderr, "from cache"
        final = cache.get(fromcache)
        for lang in final:
            position[lang] = min(10,len(final[lang]))
        cache.set(id + "position", position)
        #position = cache.get(str(request.user.id) + "position")"""
    output = dict()
    #print (final.keys(), shown_langs, position,file=sys.stderr)
 
    for item in final:
        output[item] = final[item][max(0,position[item]-10):position[item]]
    
    context = {'forsearch': input, 'langs': list(final.keys()),
               'debug': p, 'array': output, 'hide_morebutton': {item: position[item] == len(final[item]) for item in final} }
    json_out = json.dumps(context)
    print (time.time() - sec)
    return HttpResponse(json_out, content_type='application/json')

def load_more(request):
    id = request.session.session_key
    #print (id,file=sys.stderr)
    fromcache = cache.get(id + "findme")
    final = cache.get(id)
    #cache.set(id, final)
    if final:
        langs = final.keys()
        position = cache.get(id + "position")
        update_lang = request.GET['lang']
        #print (update_lang,file=sys.stderr)
        output = dict()
        if 0:#update_lang == "all":
            """delta = { item: 10 for item in langs }
            process = []
            for key in delta:
                if position[key] + 10 < len(final[key]):
                    None
                elif position[key] < len(final[key]):
                    delta[key] = len(final[key]) - position[key]
                else:
                    delta[key] = 0
                process += [[key, item] for item in final[key][position[key]:position[key] + delta]]
            process = """
            None
        else:
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
        cache.set(id + "position", position, cache_time)
        json_out = json.dumps(context)
    else:
        #print ("no final", id, fromcache,file=sys.stderr)
        json_out = json.dumps({})
    return HttpResponse(json_out, content_type='application/json')

def func(score):

    return 100 * (1 - score)

def send_report(request):
    print >>sys.stderr, request.POST, 1
    send_mail('From ' + request.POST['name'], request.POST['message'], request.POST['email'],
    ['trdmrks@yandex.ru'], fail_silently=False)
    return HttpResponse()
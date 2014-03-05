from django.shortcuts import render

from django.http import HttpResponse
from trademarks.models import Word
from trademarks.eng_eng import *

def home(request):
    context = {'forsearch': ''}
    return render(request, 'index.html', context)

def search(request):
    input = request.GET['findme']
    p = DoubleMetaphon(input).transcription
    if p == '':
        te = list()
    else: 
        raw = list(Word.objects.filter(ipa__contains=p))
        raw2 = list()
        for i in [0,1,2]:
            raw2.append(list())
        for item in raw: 
            if item.ipa == p:
                raw2[0].append(item)
            elif item.ipa.startswith(p):
                raw2[1].append(item)
            else:
                raw2[2].append(item)
        te = raw2[0] + raw2[1] + raw2[2]
    p = input + ': [' + p + ']'
    context = {'text' : p, 'array' : te, 'forsearch': input}
    return render(request, 'search.html', context)

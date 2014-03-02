from django.shortcuts import render

from django.http import HttpResponse
from trademarks.models import Word
from trademarks.eng_eng import *

def home(request):
    context = {}
    return render(request, 'index.html', context)

def search(request):
    p = DoubleMetaphon(request.POST['findme']).transcription
    if p == '':
        te = list()
    else: 
        te = list(Word.objects.filter(ipa=p))
        te += [item for item in list(Word.objects.filter(ipa__startswith=p)) if item not in te]
        te += [item for item in list(Word.objects.filter(ipa__contains=p)) if item not in te]
    p = request.POST['findme'] + ': [' + p + ']'
    context = {'text' : p, 'array' : te}
    return render(request, 'search.html', context)

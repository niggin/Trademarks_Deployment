from django.shortcuts import render

from django.http import HttpResponse
from trademarks.models import Word
from trademarks.eng_eng import *

def home(request):
    context = {}
    return render(request, 'index.html', context)

def search(request):
    p = DoubleMetaphon(request.POST['findme']).transcription 
    te = list(Word.objects.filter(ipa__startswith=p))
    p = request.POST['findme'] + ': [' + p + ']'
    context = {'text' : p, 'array' : te}
    return render(request, 'search.html', context)

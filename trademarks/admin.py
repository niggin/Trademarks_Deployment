from django.contrib import admin

from trademarks.models import Word, History

class WordAdmin(admin.ModelAdmin):
    fieldssets = [
        (None, {'fields': ['word']}),
        ('Transcription', {'fields': ['ipa']}),
        ('Definition', {'fields': ['meaning']}),
    ]
    list_display = ('word', 'ipa', 'meaning')
    search_field = ['word']

class HistoryAdmin(admin.ModelAdmin):
    fieldssets = [
        (None, {'fields': ['word', 'requests']}),
        #('Transcription', {'fields': ['ipa']}),
        #('Definition', {'fields': ['meaning']}),
    ]
    list_display = ('word', 'requests')
    search_field = ['word']

admin.site.register(Word, WordAdmin)
admin.site.register(History, HistoryAdmin)

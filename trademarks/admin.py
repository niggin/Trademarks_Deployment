from django.contrib import admin

from trademarks.models import Word

class WordAdmin(admin.ModelAdmin):
    fieldssets = [
        (None, {'fields': ['word']}),
        ('Transcription', {'fields': ['ipa']}),
        ('Definition', {'fields': ['meaning']}),
    ]
    list_display = ('word', 'ipa', 'meaning')
    search_field = ['word']

admin.site.register(Word, WordAdmin)

from django.contrib import admin

from trademarks.models import Word, History, Session, UserReaction


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
    ]
    list_display = ('word', 'requests')
    search_field = ['word']


class SessionAdmin(admin.ModelAdmin):
    fieldssets = [
        (None, {'fields': ['word', 'user_id']}),
    ]
    list_display = ('word', 'user_id')
    search_field = ['word', 'user_id']

class UserReactionAdmin(admin.ModelAdmin):
    fieldssets = [
        (None, {'fields': ['input_word', 'to_word', 'like', 'dislike']}),
    ]
    list_display = ('input_word', 'to_word', 'like', 'dislike')
    search_field = ['input_word', 'to_word']


admin.site.register(Word, WordAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(UserReaction, UserReactionAdmin)
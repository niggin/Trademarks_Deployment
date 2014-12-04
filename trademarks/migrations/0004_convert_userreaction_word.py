# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        for userreaction in orm.UserReaction.objects.all():
            userreaction.user_word = orm.History.objects.get(word=userreaction.input_word)
            userreaction.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'trademarks.history': {
            'Meta': {'object_name': 'History'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requests': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'word': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'trademarks.session': {
            'Meta': {'object_name': 'Session'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trademarks.History']"})
        },
        u'trademarks.userreaction': {
            'Meta': {'object_name': 'UserReaction'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dislike': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_word': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'like': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'to_word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trademarks.Word']"}),
            'user_word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trademarks.History']", 'null': 'True'})
        },
        u'trademarks.word': {
            'Meta': {'object_name': 'Word'},
            'fullipa': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipa': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'meaning': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'meaning_eng': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'transcription': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['trademarks']
    symmetrical = True

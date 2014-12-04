# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'History.date'
        db.add_column(u'trademarks_history', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 12, 4, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Session.date'
        db.add_column(u'trademarks_session', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 12, 4, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'UserReaction.date'
        db.add_column(u'trademarks_userreaction', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 12, 4, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'History.date'
        db.delete_column(u'trademarks_history', 'date')

        # Deleting field 'Session.date'
        db.delete_column(u'trademarks_session', 'date')

        # Deleting field 'UserReaction.date'
        db.delete_column(u'trademarks_userreaction', 'date')


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
            'to_word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trademarks.Word']"})
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
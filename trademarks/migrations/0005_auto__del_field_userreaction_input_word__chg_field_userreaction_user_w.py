# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UserReaction.input_word'
        db.delete_column(u'trademarks_userreaction', 'input_word')


        # Changing field 'UserReaction.user_word'
        db.alter_column(u'trademarks_userreaction', 'user_word_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['trademarks.History']))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'UserReaction.input_word'
        raise RuntimeError("Cannot reverse this migration. 'UserReaction.input_word' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'UserReaction.input_word'
        db.add_column(u'trademarks_userreaction', 'input_word',
                      self.gf('django.db.models.fields.CharField')(max_length=50),
                      keep_default=False)


        # Changing field 'UserReaction.user_word'
        db.alter_column(u'trademarks_userreaction', 'user_word_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trademarks.History'], null=True))

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
            'like': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'to_word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trademarks.Word']"}),
            'user_word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trademarks.History']"})
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
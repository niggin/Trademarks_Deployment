# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Word'
        db.create_table(u'trademarks_word', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('word', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ipa', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('meaning', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('meaning_eng', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('transcription', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('fullipa', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'trademarks', ['Word'])

        # Adding model 'History'
        db.create_table(u'trademarks_history', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('word', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('requests', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'trademarks', ['History'])

        # Adding model 'Session'
        db.create_table(u'trademarks_session', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('word', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trademarks.History'])),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'trademarks', ['Session'])

        # Adding model 'UserReaction'
        db.create_table(u'trademarks_userreaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('input_word', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('to_word', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trademarks.Word'])),
            ('like', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('dislike', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'trademarks', ['UserReaction'])


    def backwards(self, orm):
        # Deleting model 'Word'
        db.delete_table(u'trademarks_word')

        # Deleting model 'History'
        db.delete_table(u'trademarks_history')

        # Deleting model 'Session'
        db.delete_table(u'trademarks_session')

        # Deleting model 'UserReaction'
        db.delete_table(u'trademarks_userreaction')


    models = {
        u'trademarks.history': {
            'Meta': {'object_name': 'History'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requests': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'word': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'trademarks.session': {
            'Meta': {'object_name': 'Session'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trademarks.History']"})
        },
        u'trademarks.userreaction': {
            'Meta': {'object_name': 'UserReaction'},
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
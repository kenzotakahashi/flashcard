# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CardSet'
        db.create_table(u'flash_cardset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('visibleTo', self.gf('django.db.models.fields.CharField')(default='me', max_length=2)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastModified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('view', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=24, null=True, blank=True)),
        ))
        db.send_create_signal(u'flash', ['CardSet'])

        # Adding model 'Question'
        db.create_table(u'flash_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('questionType', self.gf('django.db.models.fields.CharField')(max_length=24, blank=True)),
            ('cardSet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flash.CardSet'], blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastModified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('choice1', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('choice2', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('choice3', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('choice4', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('choice5', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('isAnswer1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isAnswer2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isAnswer3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isAnswer4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isAnswer5', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'flash', ['Question'])

        # Adding model 'Test'
        db.create_table(u'flash_test', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastModified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'flash', ['Test'])

        # Adding M2M table for field questions on 'Test'
        m2m_table_name = db.shorten_name(u'flash_test_questions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('test', models.ForeignKey(orm[u'flash.test'], null=False)),
            ('question', models.ForeignKey(orm[u'flash.question'], null=False))
        ))
        db.create_unique(m2m_table_name, ['test_id', 'question_id'])

        # Adding model 'UserProfile'
        db.create_table(u'flash_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'flash', ['UserProfile'])


    def backwards(self, orm):
        # Deleting model 'CardSet'
        db.delete_table(u'flash_cardset')

        # Deleting model 'Question'
        db.delete_table(u'flash_question')

        # Deleting model 'Test'
        db.delete_table(u'flash_test')

        # Removing M2M table for field questions on 'Test'
        db.delete_table(db.shorten_name(u'flash_test_questions'))

        # Deleting model 'UserProfile'
        db.delete_table(u'flash_userprofile')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'flash.cardset': {
            'Meta': {'object_name': 'CardSet'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastModified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'view': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'visibleTo': ('django.db.models.fields.CharField', [], {'default': "'me'", 'max_length': '2'})
        },
        u'flash.question': {
            'Meta': {'object_name': 'Question'},
            'cardSet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['flash.CardSet']", 'blank': 'True'}),
            'choice1': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'choice2': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'choice3': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'choice4': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'choice5': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isAnswer1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isAnswer2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isAnswer3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isAnswer4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isAnswer5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lastModified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'questionType': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'})
        },
        u'flash.test': {
            'Meta': {'object_name': 'Test'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastModified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['flash.Question']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'flash.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['flash']
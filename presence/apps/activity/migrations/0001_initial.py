# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Activity'
        db.create_table('activity_activity', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='activity', to=orm['auth.User'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('to_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='activity_for_user', null=True, to=orm['auth.User'])),
            ('action', self.gf('django.db.models.fields.IntegerField')()),
            ('obj_id', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('obj2_id', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('obj3_id', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('obj4_id', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('obj5_id', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('data_for_template_cached', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('activity', ['Activity'])

        # Adding model 'NotifySettings'
        db.create_table('activity_notifysettings', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='notify_settings', unique=True, to=orm['auth.User'])),
            ('frequency', self.gf('django.db.models.fields.IntegerField')(default=86400)),
            ('last_sended', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('activity', ['NotifySettings'])

        # Adding M2M table for field immediately on 'NotifySettings'
        db.create_table('activity_notifysettings_immediately', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('notifysettings', models.ForeignKey(orm['activity.notifysettings'], null=False)),
            ('contenttype', models.ForeignKey(orm['contenttypes.contenttype'], null=False))
        ))
        db.create_unique('activity_notifysettings_immediately', ['notifysettings_id', 'contenttype_id'])


    def backwards(self, orm):
        
        # Deleting model 'Activity'
        db.delete_table('activity_activity')

        # Deleting model 'NotifySettings'
        db.delete_table('activity_notifysettings')

        # Removing M2M table for field immediately on 'NotifySettings'
        db.delete_table('activity_notifysettings_immediately')


    models = {
        'activity.activity': {
            'Meta': {'ordering': "('-time',)", 'object_name': 'Activity'},
            'action': ('django.db.models.fields.IntegerField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'data_for_template_cached': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'obj2_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'obj3_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'obj4_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'obj5_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'obj_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'activity_for_user'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activity'", 'to': "orm['auth.User']"})
        },
        'activity.notifysettings': {
            'Meta': {'ordering': "['user']", 'object_name': 'NotifySettings'},
            'frequency': ('django.db.models.fields.IntegerField', [], {'default': '86400'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'immediately': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'last_sended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'notify_settings'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['activity']

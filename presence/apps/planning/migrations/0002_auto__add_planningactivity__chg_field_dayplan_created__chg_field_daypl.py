# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PlanningActivity'
        db.create_table('planning_planningactivity', (
            ('activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['activity.Activity'], unique=True, primary_key=True)),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planning.DayPlan'])),
        ))
        db.send_create_signal('planning', ['PlanningActivity'])

        # Changing field 'DayPlan.created'
        db.alter_column('planning_dayplan', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'DayPlan.start_date'
        db.alter_column('planning_dayplan', 'start_date', self.gf('django.db.models.fields.TimeField')(null=True))


    def backwards(self, orm):
        
        # Deleting model 'PlanningActivity'
        db.delete_table('planning_planningactivity')

        # Changing field 'DayPlan.created'
        db.alter_column('planning_dayplan', 'created', self.gf('django.db.models.fields.TimeField')(auto_now_add=True))

        # Changing field 'DayPlan.start_date'
        db.alter_column('planning_dayplan', 'start_date', self.gf('django.db.models.fields.DateTimeField')(null=True))


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
        },
        'planning.dayplan': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'DayPlan'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'end_date': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'work_status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'planning.planningactivity': {
            'Meta': {'ordering': "('-time',)", 'object_name': 'PlanningActivity', '_ormbases': ['activity.Activity']},
            'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['activity.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planning.DayPlan']"})
        }
    }

    complete_apps = ['planning']

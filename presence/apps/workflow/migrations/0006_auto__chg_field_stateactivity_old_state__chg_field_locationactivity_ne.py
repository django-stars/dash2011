# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'StateActivity.old_state'
        db.alter_column('workflow_stateactivity', 'old_state_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['workflow.State']))

        # Changing field 'LocationActivity.new_location'
        db.alter_column('workflow_locationactivity', 'new_location_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflow.Location']))

        # Changing field 'LocationActivity.old_location'
        db.alter_column('workflow_locationactivity', 'old_location_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['workflow.Location']))

        # Changing field 'ProjectActivity.old_project'
        db.alter_column('workflow_projectactivity', 'old_project_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['workflow.Project']))


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'StateActivity.old_state'
        raise RuntimeError("Cannot reverse this migration. 'StateActivity.old_state' and its values cannot be restored.")

        # Changing field 'LocationActivity.new_location'
        db.alter_column('workflow_locationactivity', 'new_location_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflow.State']))

        # User chose to not deal with backwards NULL issues for 'LocationActivity.old_location'
        raise RuntimeError("Cannot reverse this migration. 'LocationActivity.old_location' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ProjectActivity.old_project'
        raise RuntimeError("Cannot reverse this migration. 'ProjectActivity.old_project' and its values cannot be restored.")


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
        'workflow.location': {
            'Meta': {'object_name': 'Location'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'workflow.locationactivity': {
            'Meta': {'ordering': "('-time',)", 'object_name': 'LocationActivity', '_ormbases': ['activity.Activity']},
            'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['activity.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'new_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'new_location_activity'", 'to': "orm['workflow.Location']"}),
            'old_location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'old_location_activity'", 'null': 'True', 'to': "orm['workflow.Location']"}),
            'old_location_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'workflow.nextstate': {
            'Meta': {'object_name': 'NextState'},
            'current_state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'next_states'", 'to': "orm['workflow.State']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'next_state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'previous_states'", 'to': "orm['workflow.State']"})
        },
        'workflow.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'workflow.projectactivity': {
            'Meta': {'ordering': "('-time',)", 'object_name': 'ProjectActivity', '_ormbases': ['activity.Activity']},
            'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['activity.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'new_project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'new_project_activity'", 'to': "orm['workflow.Project']"}),
            'old_project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'old_project_activity'", 'null': 'True', 'to': "orm['workflow.Project']"}),
            'old_project_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'workflow.state': {
            'Meta': {'ordering': "('name',)", 'object_name': 'State'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_work_state': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'workflow.stateactivity': {
            'Meta': {'ordering': "('-time',)", 'object_name': 'StateActivity', '_ormbases': ['activity.Activity']},
            'activity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['activity.Activity']", 'unique': 'True', 'primary_key': 'True'}),
            'new_state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'new_state_activity'", 'to': "orm['workflow.State']"}),
            'old_state': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'old_state_activity'", 'null': 'True', 'to': "orm['workflow.State']"}),
            'old_state_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'workflow.statelog': {
            'Meta': {'ordering': "('start',)", 'object_name': 'StateLog'},
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflow.Location']", 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflow.Project']", 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflow.State']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['workflow']

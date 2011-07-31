# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'State'
        db.create_table('workflow_state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('is_work_state', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('usual_duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('max_duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('workflow', ['State'])

        # Adding model 'NextState'
        db.create_table('workflow_nextstate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('current_state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='next_states', to=orm['workflow.State'])),
            ('next_state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='previous_states', to=orm['workflow.State'])),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('workflow', ['NextState'])

        # Adding model 'Project'
        db.create_table('workflow_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('workflow', ['Project'])

        # Adding M2M table for field members on 'Project'
        db.create_table('workflow_project_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['workflow.project'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('workflow_project_members', ['project_id', 'user_id'])

        # Adding model 'Location'
        db.create_table('workflow_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('workflow', ['Location'])

        # Adding model 'StateLog'
        db.create_table('workflow_statelog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflow.State'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflow.Project'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflow.Location'], null=True, blank=True)),
        ))
        db.send_create_signal('workflow', ['StateLog'])

        # Adding model 'StateActivity'
        db.create_table('workflow_stateactivity', (
            ('activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['activity.Activity'], unique=True, primary_key=True)),
            ('new_state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='new_state_activity', to=orm['workflow.State'])),
            ('old_state', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='old_state_activity', null=True, to=orm['workflow.State'])),
            ('old_state_start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('workflow', ['StateActivity'])

        # Adding model 'ProjectActivity'
        db.create_table('workflow_projectactivity', (
            ('activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['activity.Activity'], unique=True, primary_key=True)),
            ('new_project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='new_project_activity', to=orm['workflow.Project'])),
            ('old_project', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='old_project_activity', null=True, to=orm['workflow.Project'])),
            ('old_project_start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('workflow', ['ProjectActivity'])

        # Adding model 'LocationActivity'
        db.create_table('workflow_locationactivity', (
            ('activity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['activity.Activity'], unique=True, primary_key=True)),
            ('new_location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='new_location_activity', to=orm['workflow.Location'])),
            ('old_location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='old_location_activity', null=True, to=orm['workflow.Location'])),
            ('old_location_start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('workflow', ['LocationActivity'])


    def backwards(self, orm):
        
        # Deleting model 'State'
        db.delete_table('workflow_state')

        # Deleting model 'NextState'
        db.delete_table('workflow_nextstate')

        # Deleting model 'Project'
        db.delete_table('workflow_project')

        # Removing M2M table for field members on 'Project'
        db.delete_table('workflow_project_members')

        # Deleting model 'Location'
        db.delete_table('workflow_location')

        # Deleting model 'StateLog'
        db.delete_table('workflow_statelog')

        # Deleting model 'StateActivity'
        db.delete_table('workflow_stateactivity')

        # Deleting model 'ProjectActivity'
        db.delete_table('workflow_projectactivity')

        # Deleting model 'LocationActivity'
        db.delete_table('workflow_locationactivity')


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
            'max_duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'usual_duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflow.State']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['workflow']

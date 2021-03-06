# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Location'
        db.create_table('ddsc_core_location', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=12, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description', self.gf('django.db.models.fields.TextField')(default=u'')),
            ('point_geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(dim=3, null=True)),
            ('real_geometry', self.gf('django.contrib.gis.db.models.fields.GeometryField')(dim=3, null=True)),
            ('geometry_precision', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal('ddsc_core', ['Location'])

        # Adding model 'Timeseries'
        db.create_table('ddsc_core_timeseries', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=64, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default=u'')),
            ('supplying_system', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'timeseries', null=True, to=orm['auth.User'])),
            ('value_type', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'timeseries', null=True, to=orm['ddsc_core.Location'])),
        ))
        db.send_create_signal('ddsc_core', ['Timeseries'])


    def backwards(self, orm):
        
        # Deleting model 'Location'
        db.delete_table('ddsc_core_location')

        # Deleting model 'Timeseries'
        db.delete_table('ddsc_core_timeseries')


    models = {
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 16, 4, 51, 8, 54797)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 16, 4, 51, 8, 54727)'}),
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
        'ddsc_core.location': {
            'Meta': {'object_name': 'Location'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '12', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'geometry_precision': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'point_geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'dim': '3', 'null': 'True'}),
            'real_geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {'dim': '3', 'null': 'True'})
        },
        'ddsc_core.timeseries': {
            'Meta': {'object_name': 'Timeseries'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'timeseries'", 'null': 'True', 'to': "orm['ddsc_core.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'supplying_system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'timeseries'", 'null': 'True', 'to': "orm['auth.User']"}),
            'value_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['ddsc_core']

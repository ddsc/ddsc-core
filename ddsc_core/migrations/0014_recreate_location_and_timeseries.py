# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field data_set on 'Timeseries'
        db.delete_table(u'ddsc_core_timeseries_data_set')

        # Deleting model 'Timeseries'
        db.delete_table(u'ddsc_core_timeseries')

        # Deleting model 'Location'
        db.delete_table(u'ddsc_core_location')

        # Adding model 'Location'
        db.create_table(u'ddsc_core_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('point_geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(dim=3, null=True, blank=True)),
            ('real_geometry', self.gf('django.contrib.gis.db.models.fields.GeometryField')(dim=3, null=True, blank=True)),
            ('geometry_precision', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'ddsc_core', ['Location'])

        # Adding model 'Timeseries'
        db.create_table(u'ddsc_core_timeseries', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default=u'', blank=True)),
            ('supplying_system', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'timeseries', null=True, to=orm['auth.User'])),
            ('value_type', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'timeseries', null=True, to=orm['ddsc_core.Location'])),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.Parameter'], null=True, blank=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.Unit'], null=True, blank=True)),
            ('reference_frame', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.ReferenceFrame'], null=True, blank=True)),
            ('compartment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.Compartment'], null=True, blank=True)),
            ('measuring_device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.MeasuringDevice'], null=True, blank=True)),
            ('measuring_method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.MeasuringMethod'], null=True, blank=True)),
            ('processing_method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.ProcessingMethod'], null=True, blank=True)),
            ('first_value_timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('latest_value_number', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('latest_value_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('latest_value_timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'ddsc_core', ['Timeseries'])

        # Adding M2M table for field data_set on 'Timeseries'
        db.create_table(u'ddsc_core_timeseries_data_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('timeseries', models.ForeignKey(orm[u'ddsc_core.timeseries'], null=False)),
            ('dataset', models.ForeignKey(orm['lizard_security.dataset'], null=False))
        ))

        db.create_unique(u'ddsc_core_location', ['code'])

        db.create_unique(u'ddsc_core_timeseries', ['code'])

        db.create_unique(u'ddsc_core_timeseries_data_set', ['timeseries_id', 'dataset_id'])


    def backwards(self, orm):
        # Removing M2M table for field data_set on 'Timeseries'
        db.delete_table(u'ddsc_core_timeseries_data_set')

        # Deleting model 'Timeseries'
        db.delete_table(u'ddsc_core_timeseries')

        # Deleting model 'Location'
        db.delete_table(u'ddsc_core_location')


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
        u'ddsc_core.compartment': {
            'Meta': {'ordering': "[u'description']", 'object_name': 'Compartment'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'})
        },
        u'ddsc_core.location': {
            'Meta': {'object_name': 'Location'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'geometry_precision': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'point_geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'dim': '3', 'null': 'True', 'blank': 'True'}),
            'real_geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {'dim': '3', 'null': 'True', 'blank': 'True'})
        },
        u'ddsc_core.measuringdevice': {
            'Meta': {'ordering': "[u'description']", 'object_name': 'MeasuringDevice'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ddsc_core.measuringmethod': {
            'Meta': {'ordering': "[u'description']", 'object_name': 'MeasuringMethod'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'titel': ('django.db.models.fields.CharField', [], {'max_length': '600', 'null': 'True'})
        },
        u'ddsc_core.parameter': {
            'Meta': {'ordering': "[u'description']", 'object_name': 'Parameter'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'cas_number': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sikb_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True'})
        },
        u'ddsc_core.processingmethod': {
            'Meta': {'ordering': "[u'description']", 'object_name': 'ProcessingMethod'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ddsc_core.referenceframe': {
            'Meta': {'ordering': "[u'description']", 'object_name': 'ReferenceFrame'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ddsc_core.timeseries': {
            'Meta': {'object_name': 'Timeseries'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'compartment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Compartment']", 'null': 'True', 'blank': 'True'}),
            'data_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_security.DataSet']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'first_value_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_value_number': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'latest_value_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'latest_value_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'timeseries'", 'null': 'True', 'to': u"orm['ddsc_core.Location']"}),
            'measuring_device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.MeasuringDevice']", 'null': 'True', 'blank': 'True'}),
            'measuring_method': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.MeasuringMethod']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Parameter']", 'null': 'True', 'blank': 'True'}),
            'processing_method': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.ProcessingMethod']", 'null': 'True', 'blank': 'True'}),
            'reference_frame': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.ReferenceFrame']", 'null': 'True', 'blank': 'True'}),
            'supplying_system': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'timeseries'", 'null': 'True', 'to': "orm['auth.User']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Unit']", 'null': 'True', 'blank': 'True'}),
            'value_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        u'ddsc_core.unit': {
            'Meta': {'ordering': "[u'description']", 'object_name': 'Unit'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'conversion_factor': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'dimension': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'lizard_security.dataset': {
            'Meta': {'ordering': "['name']", 'object_name': 'DataSet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        }
    }

    complete_apps = ['ddsc_core']
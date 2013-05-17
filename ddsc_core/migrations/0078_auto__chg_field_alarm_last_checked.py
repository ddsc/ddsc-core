# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Alarm.last_checked'
        db.alter_column(u'ddsc_core_alarm', 'last_checked', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'Alarm.last_checked'
        db.alter_column(u'ddsc_core_alarm', 'last_checked', self.gf('django.db.models.fields.DateTimeField')())

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
        u'ddsc_core.alarm': {
            'Meta': {'object_name': 'Alarm'},
            'active_status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_cr': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'null': 'True', 'blank': 'True'}),
            'first_born': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'frequency': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'logical_check': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'message_type': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'previous_alarm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Alarm']", 'null': 'True', 'blank': 'True'}),
            'single_or_group': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['contenttypes.ContentType']"}),
            'template': ('django.db.models.fields.TextField', [], {'default': "u'this is a alarm message template'"}),
            'urgency': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        u'ddsc_core.alarm_active': {
            'Meta': {'object_name': 'Alarm_Active'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'alarm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Alarm']"}),
            'deactivated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1900, 1, 1, 0, 0)'}),
            'first_triggered_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1900, 1, 1, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {})
        },
        u'ddsc_core.alarm_item': {
            'Meta': {'object_name': 'Alarm_Item'},
            'alarm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Alarm']"}),
            'alarm_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['contenttypes.ContentType']"}),
            'comparision': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'first_born': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logical_check': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'value_bool': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'value_double': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_int': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value_text': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'value_type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'ddsc_core.compartment': {
            'Meta': {'ordering': "[u'description']", 'object_name': 'Compartment'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'ddsc_core.folder': {
            'Meta': {'object_name': 'Folder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        u'ddsc_core.idmapping': {
            'Meta': {'object_name': 'IdMapping'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'timeseries': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Timeseries']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        u'ddsc_core.ipaddress': {
            'Meta': {'object_name': 'IPAddress'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        u'ddsc_core.location': {
            'Meta': {'object_name': 'Location'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geometry_precision': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_index': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'point_geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '4258', 'null': 'True', 'blank': 'True'}),
            'real_geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {'srid': '4258', 'null': 'True', 'blank': 'True'}),
            'relative_location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'show_on_map': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'blank': 'True'})
        },
        u'ddsc_core.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'location_types'", 'blank': 'True', 'to': u"orm['ddsc_core.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        u'ddsc_core.logicalgroup': {
            'Meta': {'ordering': "[u'owner', u'name']", 'unique_together': "((u'owner', u'name'),)", 'object_name': 'LogicalGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_security.DataOwner']"}),
            'timeseries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'logical_groups'", 'blank': 'True', 'to': u"orm['ddsc_core.Timeseries']"})
        },
        u'ddsc_core.logicalgroupedge': {
            'Meta': {'unique_together': "((u'child', u'parent'),)", 'object_name': 'LogicalGroupEdge'},
            'child': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'parents'", 'to': u"orm['ddsc_core.LogicalGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'childs'", 'to': u"orm['ddsc_core.LogicalGroup']"})
        },
        u'ddsc_core.logrecord': {
            'Meta': {'object_name': 'LogRecord'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'}),
            'line': ('django.db.models.fields.SmallIntegerField', [], {}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        u'ddsc_core.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'ddsc_core.measuringdevice': {
            'Meta': {'ordering': "[u'description']", 'object_name': 'MeasuringDevice'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'ddsc_core.measuringmethod': {
            'Meta': {'ordering': "[u'description']", 'object_name': 'MeasuringMethod'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'titel': ('django.db.models.fields.CharField', [], {'max_length': '600', 'null': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'ddsc_core.parameter': {
            'Meta': {'ordering': "[u'description']", 'object_name': 'Parameter'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'cas_number': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sikb_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'ddsc_core.processingmethod': {
            'Meta': {'ordering': "[u'description']", 'object_name': 'ProcessingMethod'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'ddsc_core.referenceframe': {
            'Meta': {'ordering': "[u'description']", 'object_name': 'ReferenceFrame'},
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'ddsc_core.source': {
            'Meta': {'object_name': 'Source'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'frequency': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Manufacturer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'source_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'blank': 'True'})
        },
        u'ddsc_core.sourcegroup': {
            'Meta': {'object_name': 'SourceGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ddsc_core.Source']", 'symmetrical': 'False'})
        },
        u'ddsc_core.statuscache': {
            'Meta': {'object_name': 'StatusCache'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_val': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mean_val': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'min_val': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'modify_timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1900, 1, 1, 0, 0)'}),
            'nr_of_measurements_doubtful': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nr_of_measurements_reliable': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nr_of_measurements_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nr_of_measurements_unreliable': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status_date': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'std_val': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'timeseries': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Timeseries']"})
        },
        u'ddsc_core.timeseries': {
            'Meta': {'object_name': 'Timeseries'},
            'compartment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Compartment']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 14, 0, 0)'}),
            'data_set': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'timeseries'", 'blank': 'True', 'to': "orm['lizard_security.DataSet']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'first_value_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_value_number': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'latest_value_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'latest_value_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'timeseries'", 'null': 'True', 'to': u"orm['ddsc_core.Location']"}),
            'measuring_device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.MeasuringDevice']", 'null': 'True', 'blank': 'True'}),
            'measuring_method': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.MeasuringMethod']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_security.DataOwner']", 'null': 'True', 'blank': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Parameter']"}),
            'processing_method': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.ProcessingMethod']", 'null': 'True', 'blank': 'True'}),
            'reference_frame': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.ReferenceFrame']", 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Source']", 'null': 'True', 'blank': 'True'}),
            'supplying_systems': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'through': u"orm['ddsc_core.IdMapping']", 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Unit']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'blank': 'True'}),
            'validate_diff_hard': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'validate_diff_soft': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'validate_max_hard': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'validate_max_soft': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'validate_min_hard': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'validate_min_soft': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        u'ddsc_core.timeseriesgroup': {
            'Meta': {'object_name': 'TimeseriesGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'parameters': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ddsc_core.Parameter']", 'symmetrical': 'False'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ddsc_core.Source']", 'symmetrical': 'False'})
        },
        u'ddsc_core.timeseriesselectionrule': {
            'Meta': {'ordering': "[u'pk']", 'object_name': 'TimeseriesSelectionRule'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'criterion': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'lizard_security.dataowner': {
            'Meta': {'ordering': "['name']", 'object_name': 'DataOwner'},
            'data_managers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'lizard_security.dataset': {
            'Meta': {'ordering': "['owner', 'name']", 'unique_together': "(('owner', 'name'),)", 'object_name': 'DataSet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_security.DataOwner']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ddsc_core']
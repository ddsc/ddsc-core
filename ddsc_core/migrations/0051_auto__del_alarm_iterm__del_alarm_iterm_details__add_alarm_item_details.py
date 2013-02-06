# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Alarm_Iterm'
        db.delete_table(u'ddsc_core_alarm_iterm')

        # Deleting model 'Alarm_Iterm_Details'
        db.delete_table(u'ddsc_core_alarm_iterm_details')

        # Adding model 'Alarm_Item_Details'
        db.create_table(u'ddsc_core_alarm_item_details', (
            ('alarm_details', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ddsc_core.Alarm_Item'], unique=True, primary_key=True)),
            ('timeseries', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.Timeseries'])),
            ('logicalgroup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.LogicalGroup'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.Location'])),
        ))
        db.send_create_signal(u'ddsc_core', ['Alarm_Item_Details'])

        # Adding model 'Alarm_Item'
        db.create_table(u'ddsc_core_alarm_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alarm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.Alarm'])),
            ('property', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.Alarm_Property'])),
            ('comparision', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('value', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'ddsc_core', ['Alarm_Item'])

        # Deleting field 'Alarm.owner_group'
        db.delete_column(u'ddsc_core_alarm', 'owner_group_id')

        # Deleting field 'Alarm.date_created'
        db.delete_column(u'ddsc_core_alarm', 'date_created')

        # Deleting field 'Alarm.owner_id'
        db.delete_column(u'ddsc_core_alarm', 'owner_id_id')

        # Adding field 'Alarm.single_owner'
        db.add_column(u'ddsc_core_alarm', 'single_owner',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Alarm.group_owner'
        db.add_column(u'ddsc_core_alarm', 'group_owner',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_security.UserGroup'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Alarm.date_cr'
        db.add_column(u'ddsc_core_alarm', 'date_cr',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)


        # Changing field 'Alarm.previous_id'
        db.alter_column(u'ddsc_core_alarm', 'previous_id', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):
        # Adding model 'Alarm_Iterm'
        db.create_table(u'ddsc_core_alarm_iterm', (
            ('alarm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.Alarm'])),
            ('value', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('comparision', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('property_id', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'ddsc_core', ['Alarm_Iterm'])

        # Adding model 'Alarm_Iterm_Details'
        db.create_table(u'ddsc_core_alarm_iterm_details', (
            ('alarm_details', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ddsc_core.Alarm_Iterm'], unique=True, primary_key=True)),
            ('logicalgroup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.LogicalGroup'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.Location'])),
            ('timeseries', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ddsc_core.Timeseries'])),
        ))
        db.send_create_signal(u'ddsc_core', ['Alarm_Iterm_Details'])

        # Deleting model 'Alarm_Item_Details'
        db.delete_table(u'ddsc_core_alarm_item_details')

        # Deleting model 'Alarm_Item'
        db.delete_table(u'ddsc_core_alarm_item')

        # Adding field 'Alarm.owner_group'
        db.add_column(u'ddsc_core_alarm', 'owner_group',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['lizard_security.UserGroup']),
                      keep_default=False)

        # Adding field 'Alarm.date_created'
        db.add_column(u'ddsc_core_alarm', 'date_created',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=30),
                      keep_default=False)

        # Adding field 'Alarm.owner_id'
        db.add_column(u'ddsc_core_alarm', 'owner_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Alarm.single_owner'
        db.delete_column(u'ddsc_core_alarm', 'single_owner_id')

        # Deleting field 'Alarm.group_owner'
        db.delete_column(u'ddsc_core_alarm', 'group_owner_id')

        # Deleting field 'Alarm.date_cr'
        db.delete_column(u'ddsc_core_alarm', 'date_cr')


        # Changing field 'Alarm.previous_id'
        db.alter_column(u'ddsc_core_alarm', 'previous_id', self.gf('django.db.models.fields.IntegerField')())

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
            'active_stutus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_cr': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'frequency': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'group_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_security.UserGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logical_check': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'message_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'previous_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'single_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.TextField', [], {'default': "u'this is a alarm message template'"}),
            'urgency': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        u'ddsc_core.alarm_item': {
            'Meta': {'object_name': 'Alarm_Item'},
            'alarm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Alarm']"}),
            'comparision': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'property': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Alarm_Property']"}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'ddsc_core.alarm_item_details': {
            'Meta': {'object_name': 'Alarm_Item_Details'},
            'alarm_details': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ddsc_core.Alarm_Item']", 'unique': 'True', 'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Location']"}),
            'logicalgroup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.LogicalGroup']"}),
            'timeseries': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Timeseries']"})
        },
        u'ddsc_core.alarm_property': {
            'Meta': {'object_name': 'Alarm_Property'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'value_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
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
        u'ddsc_core.folder': {
            'Meta': {'object_name': 'Folder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
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
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geometry_precision': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'point_geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '4258', 'null': 'True', 'blank': 'True'}),
            'real_geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {'srid': '4258', 'null': 'True', 'blank': 'True'}),
            'relative_location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'timeseries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ddsc_core.Timeseries']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'ddsc_core.logicalgroupedge': {
            'Meta': {'unique_together': "((u'child', u'parent'),)", 'object_name': 'LogicalGroupEdge'},
            'child': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'childs'", 'to': u"orm['ddsc_core.LogicalGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'parents'", 'to': u"orm['ddsc_core.LogicalGroup']"})
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
        u'ddsc_core.source': {
            'Meta': {'object_name': 'Source'},
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Manufacturer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'source_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'blank': 'True'})
        },
        u'ddsc_core.sourcegroup': {
            'Meta': {'object_name': 'SourceGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ddsc_core.Source']", 'symmetrical': 'False'})
        },
        u'ddsc_core.timeseries': {
            'Meta': {'object_name': 'Timeseries'},
            'compartment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ddsc_core.Compartment']", 'null': 'True', 'blank': 'True'}),
            'data_set': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'timeseries'", 'symmetrical': 'False', 'to': "orm['lizard_security.DataSet']"}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'parameters': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ddsc_core.Parameter']", 'symmetrical': 'False'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ddsc_core.Source']", 'symmetrical': 'False'})
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
        },
        'lizard_security.usergroup': {
            'Meta': {'object_name': 'UserGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'managed_user_groups'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_group_memberships'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        }
    }

    complete_apps = ['ddsc_core']
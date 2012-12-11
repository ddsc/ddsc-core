# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Unit'
        db.create_table(u'ddsc_core_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=12)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('begin_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=60, null=True)),
            ('dimension', self.gf('django.db.models.fields.CharField')(max_length=12, null=True)),
            ('conversion_factor', self.gf('django.db.models.fields.CharField')(max_length=12, null=True)),
        ))
        db.send_create_signal(u'ddsc_core', ['Unit'])


    def backwards(self, orm):
        # Deleting model 'Unit'
        db.delete_table(u'ddsc_core_unit')


    models = {
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
        }
    }

    complete_apps = ['ddsc_core']
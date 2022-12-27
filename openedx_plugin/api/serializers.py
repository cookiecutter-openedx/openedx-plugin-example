"""
written by: Lawrence McDaniel
            https://lawrencemcdaniel.com

date:       jun-2019

usage:      implements a simple REST API using Django RestFramework
"""
from __future__ import absolute_import
from rest_framework import serializers
from openedx_plugin.models import Configuration


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Configuration
        fields = "__all__"

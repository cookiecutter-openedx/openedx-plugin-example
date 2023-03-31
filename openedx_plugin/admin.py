# coding=utf-8
"""
written by:     Lawrence McDaniel
                https://lawrencemcdaniel.com

date:           dec-2022

usage:          register the custom Django models in LMS Django Admin
"""
from django.contrib import admin
from .models import Configuration, Locale, MarketingSites


class MarketingSitesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MarketingSites._meta.get_fields()]


class LocaleAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Locale._meta.get_fields()]


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Configuration._meta.get_fields()]


admin.site.register(MarketingSites, MarketingSitesAdmin)
admin.site.register(Locale, LocaleAdmin)
admin.site.register(Configuration, ConfigurationAdmin)

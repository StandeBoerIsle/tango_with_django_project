# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile


class PageStyle(admin.ModelAdmin):
    field = ['title', 'category', 'url']
    list_display = ('title', 'category', 'url')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageStyle)
admin.site.register(UserProfile)

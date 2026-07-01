from django.contrib import admin
from .models import (ContactForm, Blogs, BlogCategory)

# Register your models here.

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']

# Removed Popup, Gallery, Testimonials, and Team admin classes

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'country', 'is_active']
    list_filter = ['country', 'is_active']
    search_fields = ['name', 'email', 'phone', 'country']


@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'date', 'tag', 'is_active']
    list_filter = ['category', 'date', 'is_active']
    search_fields = ['title', 'tag']
from django import template
from django.urls import reverse
import re

register = template.Library()

LANG_SUFFIX_REGEX = re.compile(r'^(.*?)/(en|ar)/?$')

@register.simple_tag(takes_context=True)
def lang_url(context, view_name, *args, **kwargs):
    """
    Returns the URL for a view with the active language suffix.
    Example: {% lang_url 'website:about' %} -> /about/en/ or /about/ar/
    Example: {% lang_url 'website:home' %} -> /en/ or /ar/
    """
    lang = kwargs.pop('lang', None)
    if not lang:
        lang = context.get('LANGUAGE_CODE') or 'en'
    if lang not in ('en', 'ar'):
        lang = 'en'
        
    url = reverse(view_name, args=args, kwargs=kwargs)
    if url == '/':
        return f'/{lang}/'
    clean_url = url.rstrip('/')
    return f'{clean_url}/{lang}/'


@register.filter
def to_lang_url(url, lang='en'):
    """
    Converts a given URL path to have the specified language suffix.
    Example: '/about/' | to_lang_url:'ar' -> '/about/ar/'
    Example: '/about/en/' | to_lang_url:'ar' -> '/about/ar/'
    """
    if not url:
        return f'/{lang}/'
    if lang not in ('en', 'ar'):
        lang = 'en'
        
    match = LANG_SUFFIX_REGEX.match(url)
    if match:
        base_path = match.group(1)
        if not base_path:
            return f'/{lang}/'
        return f'{base_path}/{lang}/'
        
    if url == '/':
        return f'/{lang}/'
        
    clean_url = url.rstrip('/')
    return f'{clean_url}/{lang}/'

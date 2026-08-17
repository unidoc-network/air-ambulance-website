from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.utils import translation
import re

class LanguageSuffixMiddleware(MiddlewareMixin):
    """
    Middleware for suffix-based language routing:
    - /en/ or /ar/ for homepage
    - /about/en/, /about/ar/, etc. for subpages
    - Automatically redirects / to /en/ or /ar/ based on saved cookie preference
    - Automatically redirects /about/ to /about/en/ or /about/ar/ based on saved cookie
    - Persists language cookies (bluedot_lang, django_language) for 1 year across sessions
    """
    # Regex to match URLs with trailing language suffix: e.g. /en/, /ar/, /about/en/, /about/ar/
    LANG_SUFFIX_REGEX = re.compile(r'^(.*?)/(en|ar)/?$')
    
    EXCLUDED_PREFIXES = (
        '/static/',
        '/media/',
        '/superadmin',
        '/sitemap.xml',
        '/fleet-sitemap.xml',
        '/robots.txt',
        '/send-otp/',
        '/verify-otp/',
        '/submit-enquiry/',
    )

    def process_request(self, request):
        path = request.path_info
        
        # 1. Skip excluded prefixes (admin, static, media, APIs)
        for prefix in self.EXCLUDED_PREFIXES:
            if path.startswith(prefix):
                return None
                
        # 2. Check if path has /en/ or /ar/ suffix
        match = self.LANG_SUFFIX_REGEX.match(path)
        if match:
            base_path = match.group(1) # e.g. "" for "/en/" or "/about" for "/about/en/"
            lang = match.group(2)      # "en" or "ar"
            
            request.LANGUAGE_CODE = lang
            translation.activate(lang)
            
            # Rewrite path_info internally so Django routes to standard URL patterns cleanly
            internal_path = (base_path if base_path else '') + '/'
            request.path_info = internal_path
            return None
            
        # 3. Path has NO language suffix
        saved_lang = request.COOKIES.get('bluedot_lang') or request.COOKIES.get('django_language') or 'en'
        if saved_lang not in ('en', 'ar'):
            saved_lang = 'en'
            
        request.LANGUAGE_CODE = saved_lang
        translation.activate(saved_lang)
        
        # For non-GET/HEAD methods (e.g. POST), do not redirect as it would break form payloads
        if request.method not in ('GET', 'HEAD'):
            return None
            
        # Preserve query string if present
        query_string = request.META.get('QUERY_STRING', '')
        query_part = f'?{query_string}' if query_string else ''
        
        # If root '/', redirect to '/en/' or '/ar/'
        if path == '/' or path == '':
            return redirect(f'/{saved_lang}/{query_part}')
            
        # If any other page without language suffix (e.g. /about/), redirect to /about/en/ or /about/ar/
        clean_path = path.rstrip('/')
        return redirect(f'{clean_path}/{saved_lang}/{query_part}')

    def process_response(self, request, response):
        lang = getattr(request, 'LANGUAGE_CODE', None)
        if lang in ('en', 'ar'):
            # Ensure cookies are set so subsequent requests/sessions remember the active language
            if request.COOKIES.get('bluedot_lang') != lang or request.COOKIES.get('django_language') != lang:
                response.set_cookie('bluedot_lang', lang, max_age=31536000, path='/')
                response.set_cookie('django_language', lang, max_age=31536000, path='/')
        return response

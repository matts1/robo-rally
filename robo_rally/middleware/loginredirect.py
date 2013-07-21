from django.http import HttpResponseRedirect
from django.conf import settings
from django.core import urlresolvers

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page in
    LOGIN_REQUIRED_URLS, and to not be authenticated to view any page in
    NO_LOGIN_REQUIRED_URLS, both of which are in setting.py.

    Those variables contain the names of the urls as specified in urls.py.
    """
    def process_request(self, request):
        path = request.path_info.lstrip('/')

        res = urlresolvers.get_resolver(settings.ROOT_URLCONF)
        for pattern in res.url_patterns:
            if pattern.regex.match(path) and hasattr(pattern, 'name'):
                logged_in = request.user.is_authenticated()
                if logged_in and pattern.name in settings.NO_LOGIN_REQUIRED_URLS:
                    return HttpResponseRedirect(settings.HOME_URL)
                if not logged_in and pattern.name in settings.LOGIN_REQUIRED_URLS:
                    return HttpResponseRedirect(settings.LOGIN_URL)

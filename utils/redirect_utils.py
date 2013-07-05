# coding: utf-8
__author__ = 'Arthur'

class RedirectUtils:
    @classmethod
    def need_redirect(self, request, flag='default_redirect'):
        if request.session[flag]:
            return True
        else:
            return False

    @classmethod
    def redirect_url(self, request, flag='default_redirect'):
        return request.session[flag]

    @classmethod
    def set_url_to_redirect(self, request, url, flag='default_redirect'):
        request.session[flag] = url

    @classmethod
    def remove_redirect_url(self, request, flag='default_redirect'):
        request.session[flag] = None
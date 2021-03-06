import inspect
import logging
import traceback
from types import new_class

import re
from django.conf.urls import url

from django.conf import settings

from shark.common import listify
from shark.handler import markdown_preview, BaseHandler, shark_django_handler, StaticPage, \
    SiteMap, GoogleVerification, BingVerification, YandexVerification, shark_django_redirect_handler, Favicon, \
    shark_django_handler_no_csrf
from shark.settings import SharkSettings


def get_urls():
    urlpatterns = []
    redirects = []

    def add_handler(obj, route=None):
        if inspect.isclass(obj) and issubclass(obj, BaseHandler) and 'route' in dir(obj):
            if route or obj.route:

                render_function = obj().render_base
                if 'csrf_exempt' in dir(render_function) and render_function.csrf_exempt:
                    render_handler = shark_django_handler_no_csrf
                else:
                    render_handler = shark_django_handler

                urlpatterns.append(url(
                    route or obj.route,
                    render_handler,
                    {'handler': obj},
                    name=obj.get_unique_name()
                ))

            for redirect_route in listify(obj.redirects):
                if isinstance(redirect_route, str):
                    redirects.append(url(redirect_route, shark_django_redirect_handler, {'handler': obj}))
                elif isinstance(redirect_route, tuple):
                    for redirect_sub_route in redirect_route[0]:
                        redirects.append(url(redirect_sub_route, shark_django_redirect_handler, {'handler': obj, 'function':redirect_route[1]}))


    apps = settings.INSTALLED_APPS
    for app_name in apps:
        try:
            app = __import__(app_name + '.views').views
        except ImportError as e:
            if not re.match(r"No module named '{}'".format(app_name + '.views'), e.msg):
                raise e
        except AttributeError as e:
            if not re.match(r"module '{}' has no attribute 'views'".format(app_name.split('.')[0]), e.args[0]):
                raise e
        else:
            objs = [getattr(app, key) for key in dir(app)]

            for obj in objs:
                add_handler(obj)

    if SharkSettings.SHARK_PAGE_HANDLER:
        handler_parts = SharkSettings.SHARK_PAGE_HANDLER.split('.')
        page_handler = __import__(handler_parts[0])
        for handler_part in handler_parts[1:]:
            page_handler = page_handler.__dict__[handler_part]

        if SharkSettings.SHARK_USE_STATIC_PAGES:
            urlpatterns.append(url(
                    '^page/(.*)$',
                    shark_django_handler,
                    {'handler': new_class('StaticPage', (StaticPage, page_handler))},
                    name='shark_static_page'
            ))

    add_handler(Favicon)
    add_handler(SiteMap)

    urlpatterns.append(url(r'^markdown_preview/$', markdown_preview, name='django_markdown_preview'))

    if SharkSettings.SHARK_GOOGLE_VERIFICATION:
        add_handler(GoogleVerification, '^{}.html$'.format(SharkSettings.SHARK_GOOGLE_VERIFICATION))

    if SharkSettings.SHARK_BING_VERIFICATION:
        add_handler(BingVerification, '^BingSiteAuth.xml$')

    if SharkSettings.SHARK_YANDEX_VERIFICATION:
        add_handler(YandexVerification, '^yandex_{}.html$'.format(SharkSettings.SHARK_YANDEX_VERIFICATION))

    urlpatterns.extend(redirects)
    return urlpatterns

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
# Copyright (c) 2008-2014 University of Dundee.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Aleksandra Tarkowska <A(dot)Tarkowska(at)dundee(dot)ac(dot)uk>, 2008.
#
# Version: 1.0
#

import logging
import pkgutil
from django.conf import settings
from django.apps import AppConfig
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import redirect

from django.urls import reverse
from django.utils.functional import lazy
from django.views.generic import RedirectView
from django.views.decorators.cache import never_cache
from omeroweb_cred.webclient import views as webclient_views
from omeroauth import views as omeroauth_views

logger = logging.getLogger(__name__)

# error handler
handler404 = ".feedback.views.handler404"
handler500 = ".feedback.views.handler500"

reverse_lazy = lazy(reverse, str)


def redirect_urlpatterns():
    """
    Helper function to return a URL pattern for index page http://host/.
    """
    if settings.INDEX_TEMPLATE is None:
        return [
            url(
                r"^$",
                never_cache(
                    RedirectView.as_view(url=reverse_lazy("webindex"), permanent=True)
                ),
                name="index",
            )
        ]
    else:
        return [
            url(
                r"^$",
                never_cache(
                    RedirectView.as_view(
                        url=reverse_lazy("webindex_custom"), permanent=True
                    )
                ),
                name="index",
            ),
        ]


# url patterns

urlpatterns = []

for app in settings.ADDITIONAL_APPS:
    if isinstance(app, AppConfig):
        app_config = app
    else:
        app_config = AppConfig.create(app)
    label = app_config.label

    # Depending on how we added the app to INSTALLED_APPS in settings.py,
    # include the urls the same way
    if ".%s" % app in settings.INSTALLED_APPS:
        urlmodule = ".%s.urls" % app
    else:
        urlmodule = "%s.urls" % app

    # Try to import module.urls.py if it exists (not for corsheaders etc.)
    urls_found = pkgutil.find_loader(urlmodule)
    if urls_found is not None:
        try:
            __import__(urlmodule)
            # https://stackoverflow.com/questions/7580220/django-urls-how-to-map-root-to-app
            if label == settings.OMEROWEB_ROOT_APPLICATION:
                regex = r"^"
            else:
                regex = "^%s/" % label
            urlpatterns.append(url(regex, include(urlmodule)))
        except ImportError:
            print(
                """Failed to import %s
Please check if the app is installed and the versions of the app and
OMERO.web are compatible
            """
                % urlmodule
            )
            raise
    else:
        logger.debug("Module not found: %s" % urlmodule)

urlpatterns += [
    url(
        r"^favicon\.ico$",
        lambda request: redirect("%s%s" % (settings.STATIC_URL, settings.FAVICON_URL)),
    ),
    url(r"^omeroauth/", include("omeroweb_cred.omeroauth.urls")),
    url(r"^webgateway/", include("omeroweb_cred.webgateway.urls")),
    url(r"^webadmin/", include("omeroweb_cred.webadmin.urls")),
    url(r"^webclient/", include("omeroweb_cred.webclient.urls")),
    url(r"^url/", include("omeroweb_cred.webredirect.urls")),
    url(r"^feedback/", include("omeroweb_cred.feedback.urls")),
    url(r"^api/", include("omeroweb_cred.api.urls")),
    url(r"^index/$", webclient_views.custom_index, name="webindex_custom"),
    url(r'^$', omeroauth_views.OauthLoginView.as_view(), name="oauth_index"),
    url(r'^callback/(?P<name>[a-z][a-z0-9]+)$',
        omeroauth_views.OauthCallbackView.as_view(), name="oauth_callback"),

    url(r'^confirm$', omeroauth_views.confirm, name="oauth_confirm"),

    url(r'^sessiontoken$', omeroauth_views.sessiontoken, name="oauth_sessiontoken"),
]

urlpatterns += redirect_urlpatterns()


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

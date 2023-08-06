#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = (
    'django.views.generic.simple',

    url(r'^$', views.OauthLoginView.as_view(), name="oauth_index"),
    url(r'^callback/(?P<name>[a-z][a-z0-9]+)$',
        views.OauthCallbackView.as_view(), name="oauth_callback"),

    url(r'^confirm$', views.confirm, name="oauth_confirm"),

    url(r'^sessiontoken$', views.sessiontoken, name="oauth_sessiontoken"),
    url(r'^create_admin_conn$', views.create_admin_conn, name="oauth_adminconn"),
    url(r'^create_session_for_user$', views.create_session_for_user, name="oauth_usersession"),

)

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^authorize-url/$',
        views.AuthorizeUrlView.as_view(),
        name='authenticate_url'),

    url(r'^authorize/$',
        views.AuthorizeView.as_view(),
        name='authenticate'),

    url(r'^authorize_callback/$',
        views.AuthorizeCallbackView.as_view(),
        name='authorize_callback'),

    url(r'^user/$',
        views.UserInfoView.as_view(),
        name='user'),
]
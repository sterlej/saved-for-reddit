"""reddit_saved URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from search import views

"""
URLconf.py - simple mapping between URL patterns(regex) to python functions (views)

How django processes a request
    When a user requests a page from site, this is algo:
    1) Django determines the root URLconf module, ordinarily this is value of ROOT_URLCONF

    2) Django loads that python module and looks for the var: urlpatterns. A list of
    django.conf.urls.url() instances.

    3) Django runs through each URL pattern, stops at first run that matches requested URL

    4) When match: Django imports and calls given view, and view gets following args
        - instance of HttpRequest
        - If the matched regular expression returned no named groups, then the matches
         from the regular expression are provided as positional arguments.
"""

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.get_latest_saved),
    # url(r'^search/', include('haystack.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls), ),
    ]

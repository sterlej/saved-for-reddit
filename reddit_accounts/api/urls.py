from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profiles/$',
        views.RedditProfileListView.as_view(),
        name='profiles_list'),
]
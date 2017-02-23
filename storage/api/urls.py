from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^savables/$',
        views.SavableListView.as_view(),
        name='savable_list'),

    url(r'^savables/(?P<pk>[0-9]+)/$',
        views.SavableDetailView.as_view(),
        name='delete')
]
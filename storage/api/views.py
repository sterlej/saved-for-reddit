from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.renderers import TemplateHTMLRenderer
from ..models import Savable
from .serializers import SavableSerializer
from rest_framework.response import Response
from rest_framework import status
from ..tasks import test


class BulkDestroyMixin(object):

    def bulk_destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset(request, *args, **kwargs)
        self.perform_bulk_destroy(queryset)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def perform_bulk_destroy(self, objects):
        for obj in objects:
            self.perform_destroy(obj)


class SavableListView(BulkDestroyMixin, ListAPIView):
    serializer_class = SavableSerializer
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'display_saved.html'

    # def get(self, request, *args, **kwargs):
    #     return Response({'object_list': self.get_queryset(*args, **kwargs)})

    def get_queryset(self, *args, **kwargs):
        profile_ids = self.request.GET.get('ids')
        if not profile_ids:
            profile_ids = []
        queryset = Savable.objects.all_user_savables(profile_ids)
        # test.delay()
        return queryset

    def delete(self, request, *args, **kwargs):
        return self.bulk_destroy(request, *args, **kwargs)


class SavableDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class =  SavableSerializer
    queryset = Savable.objects.all()

    def get_queryset(self, *args, **kwargs):
        profile_ids = self.request.GET.get('ids')
        if not profile_ids:
            profile_ids = []
        queryset = Savable.objects.all_user_savables(profile_ids)
        return queryset

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

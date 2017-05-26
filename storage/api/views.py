from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_haystack.viewsets import HaystackViewSet, HaystackGenericAPIView
from haystack.query import SearchQuerySet
from django.shortcuts import redirect


from social_django.models import UserSocialAuth

from ..models import Savable, Comment, Submission, Subreddit
from ..tasks import remove_unsaved
from .serializers import SavableSerializer, CommentCreateSerializer, SubmissionCreateSerializer, \
    SavableSearchSerializer, SubredditSerializer


class BulkDestroyMixin(object):

    def bulk_destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset(request, *args, **kwargs)
        self.perform_bulk_destroy(queryset)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def perform_bulk_destroy(self, objects):
        if objects:
            for obj in objects:
                self.perform_destroy(obj)


class BulkCreateMixin(CreateModelMixin):

    def post(self, request, *args, **kwargs):
        for data in request.data:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                serializer.instance.saved_by.add(request.user)
                http_status = status.HTTP_201_CREATED

            else:
                try:
                    saved_id = data[self.id_field]
                    saved = Savable.objects.get(pk=saved_id)
                    current_user = request.user.social_auth.last()
                    if not current_user in saved.saved_by.all():
                        saved.saved_by.add(current_user)
                        http_status = status.HTTP_202_ACCEPTED
                    else:
                        http_status = status.HTTP_304_NOT_MODIFIED
                except:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=http_status)


class SavableListView(BulkDestroyMixin, ListAPIView):
    serializer_class = SavableSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        if self.request.user.id == 9: return Savable.objects.all_prefetch()
        remove_unsaved.delay([self.request.user.id])
        return Savable.objects.all_user_savables([self.request.user.id])

    def delete(self, request, *args, **kwargs):
        return self.bulk_destroy(request, *args, **kwargs)


class SavableSearchView(ListAPIView, HaystackGenericAPIView):
    serializer_class = SavableSearchSerializer
    queryset = Savable.objects.all()

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        subreddit_ids = request.GET.getlist('sid')
        search_query_set = SearchQuerySet()

        if not q and not subreddit_ids:
            return_saved = Savable.objects.all_user_savables([self.request.user.id])

        else:
            search_query_set = search_query_set.filter(saved_by=self.request.user.id)
            if subreddit_ids:
                search_query_set = search_query_set.filter(subreddit_id__in=subreddit_ids)

            if q:
                search_query_set = search_query_set.filter(content=q)

            saved_ids = search_query_set.values_list('savable_ptr_id', flat=True)
            return_saved = Savable.objects.filter(pk__in=list(saved_ids))

        serializer = SavableSerializer(return_saved, many=True)
        return Response(serializer.data)


class CommentCreateView(BulkCreateMixin, ListCreateAPIView):
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.all()
    id_field = 'comment_id'


class SubmissionCreateView(BulkCreateMixin, ListCreateAPIView):
    serializer_class = SubmissionCreateSerializer
    queryset = Submission.objects.all()
    id_field = 'submission_id'


class SavableDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class =  SavableSerializer
    queryset = Savable.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SubredditListView(BulkDestroyMixin, ListAPIView):
    serializer_class = SubredditSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        if self.request.user.id == 9: return Subreddit.objects.all()
        return Subreddit.objects.filter(pk__in=Savable.objects.all_user_savables([self.request.user.id]).values_list(
            'subreddit', flat=True)).distinct()

    def delete(self, request, *args, **kwargs):
        return self.bulk_destroy(request, *args, **kwargs)


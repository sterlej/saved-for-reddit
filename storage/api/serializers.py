from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Savable, Subreddit, Submission, Comment
from drf_haystack.serializers import HaystackSerializer
from ..search_indexes import CommentIndex, SubmissionIndex

SAVABLE_FIELDS = ('score', 'created_utc', 'author_flair_text', 'author', 'author_user_id', 'subreddit')


class SubredditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subreddit
        fields = ('name', 'id')


# class SubredditSearchSerializer(HaystackSerializer):
#     class Meta:
#         index_classes = [SubredditIndex]
#         fields = ["name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class CommentCreateSerializer(serializers.ModelSerializer):
    subreddit = SubredditSerializer()

    class Meta:
        model = Comment
        fields = ('body', 'body_html', 'parent_id', 'comment_id', 'link_url', 'link_title', 'permalink',
                  'full_comments_url', 'link_author') + SAVABLE_FIELDS

    def create(self, validated_data):
        subreddit_data = validated_data.pop('subreddit')
        subreddit = Subreddit.objects.get_or_create(name=subreddit_data['name'])
        if subreddit[1]:
            subreddit[0].save()
        comment = Comment.objects.create(subreddit=subreddit[0], **validated_data)
        comment.save()
        return comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('body', 'body_html', 'parent_id', 'comment_id', 'link_url', 'link_title', 'permalink',
                  'full_comments_url', 'link_author')


class SubmissionCreateSerializer(serializers.ModelSerializer):
    subreddit = SubredditSerializer()

    class Meta:
        model = Submission
        fields = ('title', 'num_comments', 'url', 'permalink', 'post_hint', 'submission_id', 'thumbnail') \
                 + SAVABLE_FIELDS

    def create(self, validated_data):
        subreddit_data = validated_data.pop('subreddit')
        subreddit = Subreddit.objects.get_or_create(name=subreddit_data['name'])
        if subreddit[1]:
            subreddit[0].save()
        submission = Submission.objects.create(subreddit=subreddit[0], **validated_data)
        submission.save()
        return submission


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('title', 'num_comments', 'url', 'permalink', 'post_hint', 'submission_id', 'thumbnail')


class SavableSerializer(serializers.ModelSerializer):
    subreddit = SubredditSerializer(read_only=True)
    submission = SubmissionSerializer(required=False, read_only=True)
    comment = CommentSerializer(required=False, read_only=True)
    saved_by = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Savable
        fields = ('submission', 'comment', 'saved_by', 'id', 'is_saved') + SAVABLE_FIELDS


class SavableSearchSerializer(HaystackSerializer):

    class Meta:
        index_classes = [CommentIndex, SubmissionIndex]
        fields = ['body', 'link_title', 'savable_ptr_id', 'title']


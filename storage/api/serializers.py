from rest_framework import serializers
from ..models import Savable, Subreddit, Submission, Comment
# from django.db.models import Prefetch


class SubredditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subreddit
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('body', 'id', 'body_html')


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('title', 'num_comments', 'url', 'permalink', 'post_hint', 'id')


class SavableSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer()
    subreddit = SubredditSerializer()
    comment = CommentSerializer()
    class Meta:
        model = Savable
        fields = ('submission', 'author', 'subreddit', 'comment', 'id', 'created_utc')








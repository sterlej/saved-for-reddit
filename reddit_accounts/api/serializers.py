from rest_framework import serializers
from ..models import RedditProfile


class RedditProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedditProfile
        fields = ('reddit_user_id', 'username', 'refresh_token', 'active')


class RedditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedditProfile
        fields = ('identity', 'reddit_user_id', 'username', 'refresh_token', 'active')

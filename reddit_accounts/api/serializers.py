from rest_framework import serializers
from ..models import RedditProfile
from django.contrib.auth.models import User
from oauth2_provider.models import AccessToken
from social_django.models import UserSocialAuth


class RedditProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedditProfile
        fields = ('reddit_user_id', 'username', 'refresh_token', 'active')


class RedditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedditProfile
        fields = ('identity', 'user_social', 'user')


class UserSocialAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocialAuth
        fields = ('id', 'uid', 'extra_data')



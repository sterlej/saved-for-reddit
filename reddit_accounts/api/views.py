from utils.RedditAPIs import reddit_api
from .services import UserSocialService
from reddit_accounts.tasks import create_or_get_user, post_saved_data, get_saved_json
from storage.models import Comment, Submission
from utils.django_functions import get_model_fields
from .serializers import UserSocialAuthSerializer
from social_django.models import UserSocialAuth

from celery import chain
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect


class AuthorizeCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        auth_code = request.GET.get('code')
        access = reddit_api.get_access_information(authorization_code=auth_code)
        refresh_token = access['refresh_token']
        access_token = access['access_token']
        response = redirect('home')

        convert_token_url = request.build_absolute_uri(reverse('convert_token'))
        refresh_token_url = request.build_absolute_uri(reverse('token'))
        create_comments_url = request.build_absolute_uri(reverse('api-saved:comments_create'))
        create_submissions_url = request.build_absolute_uri(reverse('api-saved:submissions_create'))

        user_info = create_or_get_user(convert_token_url, refresh_token_url, access_token, refresh_token)
        result = chain(get_saved_json.s(user_info=user_info,
                                        refresh_token=refresh_token,
                                        comment_keys=list(get_model_fields(Comment)),
                                        submission_keys=list(get_model_fields(Submission))),
                       post_saved_data.s((create_comments_url, create_submissions_url))).apply_async()

        response.set_cookie('at', user_info['user_create_response']['access_token'])
        return response


class AuthorizeUrlView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        auth_url = reddit_api.get_user_authorization_code_url()
        return Response({'auth-url': auth_url})


class AuthorizeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        auth_url = reddit_api.get_user_authorization_code_url()
        return redirect(auth_url)


class UserInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = UserSocialAuth.objects.get(user_id=request.user.id)
        serializer = UserSocialAuthSerializer(queryset)
        return Response(serializer.data)

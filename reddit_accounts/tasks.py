from celery import task, chain, Task, group
import requests

from reddit_accounts.api.services import UserSocialService
from utils.RedditAPIs import reddit_api


@task
def create_or_get_user(convert_token_url, refresh_token_url, access_token, refresh_token):
    created = False
    reddit_api.authenticate(refresh_token)
    user_social_id = reddit_api.get_praw_user().id
    user_social_service = UserSocialService()

    if not user_social_service.user_and_social_exists(user_social_id):
        post_data = {'token': access_token,
                     'backend': 'reddit',
                     'client_id': 'xrwVR6buMLiS302PkP2gngooKPHbtHKlh2oubS1T',
                     'grant_type': 'convert_token'}
        user_create_response = requests.post(convert_token_url, data=post_data).json()
        user_social = user_social_service.get_social_user(user_social_id=user_social_id)
        user_social_service.update_social_auth_refresh_token(user_social=user_social,
                                                             refresh_token=refresh_token)
        created = True
    else:
        user_social = user_social_service.get_social_user(user_social_id=user_social_id)
        oauth_refresh_token = user_social.user.refreshtoken_set.last()
        post_data = {'refresh_token': oauth_refresh_token,
                     'client_id': 'xrwVR6buMLiS302PkP2gngooKPHbtHKlh2oubS1T',
                     'grant_type': 'refresh_token'}
        user_create_response = requests.post(refresh_token_url, data=post_data).json()

    user_info = {'created': created,
                 'user_social_id': user_social_id,
                 'user_create_response': user_create_response}
    
    return user_info


@task
def get_saved_json(user_info, refresh_token, comment_keys, submission_keys):
    reddit_api.authenticate(refresh_token)
    time = None
    limit = None

    saved_generator = reddit_api.get_saved_generator(time=time,
                                                     limit=limit)

    json_data = reddit_api.get_saved_json_data(praw_iterable=saved_generator,
                                               comment_keys=comment_keys,
                                               submission_keys=submission_keys,
                                               transform_values_func=reddit_api.transform_comment_and_submission_values)
    response = {'user_info': user_info, 'saved_data': json_data}
    return response


@task
def post_saved_data(saved_json, create_urls):
    saved_data = saved_json.pop('saved_data')
    user_social_id = saved_json['user_info']['user_social_id']
    user_social = UserSocialService().get_social_user(user_social_id)
    auth_token = user_social.user.accesstoken_set.last().token
    group([mapper.s(saved_data[key], create_urls, auth_token) for key in saved_data])()
    return saved_json


@task
def mapper(saved_json, create_urls, auth_token):
    headers = {'Authorization': 'Bearer {}'.format(auth_token)}
    if 'body' in saved_json[0]:
        create_url = create_urls[0]
    else:
        create_url = create_urls[1]
    response = requests.post(create_url,
                             headers=headers,
                             json=saved_json)




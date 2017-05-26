import praw
from uuid import uuid4
from collections import defaultdict
from datetime import datetime
from functools import partial


CLIENT_ID = "SYpUYS_j-YgJOQ"
CLIENT_SECRET = "YY0Ch-i_gxFuSzcY4q5S-VTFT20"
REDIRECT_URI = "http://localhost:8000/reddit_callback"


PRAW_NAME_TO_OBJECT_MAP = {
    'Submission': praw.objects.Submission,
    'Comment': praw.objects.Comment
}


class RedditUserAPI:

    def __init__(self):
        self.reddit_agent = self.get_unauthorized_reddit_agent()
        self._authenticated = False

    @staticmethod
    def transform_comment_and_submission_values(field_name, value):
        if value:
            if field_name == 'subreddit':
                return {'name': value.display_name}
            elif field_name == 'author':
                return value.name
            elif field_name == 'created_utc':
                return datetime.utcfromtimestamp(value).isoformat()

            elif field_name == 'thumbnail':
                if not value.startswith('http'):
                    return None

        return value

    @staticmethod
    def transform_values(transform_func, field_name, value):
        if transform_func:
            return transform_func(field_name, value)
        else:
            return value

    @staticmethod
    def get_unauthorized_reddit_agent(user_agent=None, client_id=None, client_secret=None, redirect_uri=None):
        reddit_agent = praw.Reddit(user_agent="Saved Search For Reddit v1.0 by /u/__py_dev")
        reddit_agent.set_oauth_app_info(client_id=CLIENT_ID,
                                        client_secret=CLIENT_SECRET,
                                        redirect_uri='http://127.0.0.1:8000/api/accounts/authorize_callback')
        return reddit_agent

    def get_user_authorization_code_url(self):
        url = self.reddit_agent.get_authorize_url(str(uuid4()), ('identity', 'edit', 'history', 'save'), True)
        return url

    def get_refresh_token(self, authorization_code):
        return self.reddit_agent.get_access_information(authorization_code)['refresh_token']

    def get_access_information(self, authorization_code):
        return self.reddit_agent.get_access_information(authorization_code)

    def authenticate(self, refresh_token):
        self.reddit_agent.refresh_access_information(refresh_token)
        self._authenticated = True

    def get_praw_user(self, as_dict=False):
        if self._authenticated and as_dict:
            return self.reddit_agent.user.__dict__
        elif self._authenticated:
            return self.reddit_agent.user

    def get_saved_generator(self, limit=None, time=None):
        if self._authenticated:
            if not time:
                time = 'all'
            return self.reddit_agent.user.get_saved(limit=limit, time=time)
        else:
            return None
        
    @staticmethod
    def filter_praw_objects_to_dict(praw_object_iterable, praw_object_names_to_filter):
        name_to_objects_map = defaultdict(list)

        for praw_object in praw_object_iterable:
            for object_name in praw_object_names_to_filter:
                if isinstance(praw_object, PRAW_NAME_TO_OBJECT_MAP[object_name]):
                    name_to_objects_map[object_name].append(praw_object)
        return name_to_objects_map

    def get_profile_saved(self, limit=None, time=None):
        if self._authenticated:
            saved = self.get_saved_generator(limit=limit, time=time)
            praw_name_to_objects = self.filter_praw_objects_to_dict(saved, ['Submission', 'Comment'])
            return praw_name_to_objects

    def get_saved_json_data(self, praw_iterable, comment_keys=None, submission_keys=None, transform_values_func=None):
        saved = defaultdict(list)
        if self._authenticated:
            for praw_obj in praw_iterable:
                if isinstance(praw_obj, praw.objects.Comment):
                    saved_dict = self.transform_praw_saved_to_dict(praw_obj, comment_keys, transform_values_func)

                    if saved_dict:
                        saved['comments'].append(saved_dict)

                elif isinstance(praw_obj, praw.objects.Submission):
                    saved_dict = self.transform_praw_saved_to_dict(praw_obj, submission_keys, transform_values_func)

                    if saved_dict:
                        saved['submissions'].append(saved_dict)

        return saved
    
    def transform_praw_saved_to_dict(self, praw_saved_object, fields_to_get, transform_values_func):
        saved_dict = {}
        if isinstance(praw_saved_object, praw.objects.Comment):
            saved_dict = {field: self.transform_values(transform_values_func, field, value)
                          for field, value in praw_saved_object.__dict__.items() if field in fields_to_get}
            saved_dict['comment_id'] = saved_dict.pop('id')

            if 'permalink' in fields_to_get:
                saved_dict['permalink'] = praw_saved_object.permalink

        elif isinstance(praw_saved_object, praw.objects.Submission):
            saved_dict = {field: self.transform_values(transform_values_func, field, value)
                          for field, value in praw_saved_object.__dict__.items() if field in fields_to_get}
            saved_dict['submission_id'] = saved_dict.pop('id')

        return saved_dict


reddit_api = RedditUserAPI()
# reddit_api.authenticate('63259309-sLfQxfIXwc0DeBrUWMqBpZ9PGTk')
# print(reddit_api.get_praw_user())
# saved = reddit_api.get_profile_saved()
# from pprint import pprint
#
# pprint(dir(saved['Submission'][0]))
# saved['Submission'][0].unsave()
# reddit_api.get_saved_json_data(reddit_api.get_saved_generator())


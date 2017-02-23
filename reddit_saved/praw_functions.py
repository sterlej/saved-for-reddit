import praw
from uuid import uuid4
from collections import defaultdict


CLIENT_ID = "SYpUYS_j-YgJOQ"
CLIENT_SECRET = "YY0Ch-i_gxFuSzcY4q5S-VTFT20"
REDIRECT_URI = "http://localhost:8000/reddit_callback"

PRAW_NAME_TO_OBJECT_MAP = {
    'Submission': praw.objects.Submission,
    'Comment': praw.objects.Comment
}


def get_unauthorized_reddit_agent():
    reddit_agent = praw.Reddit(user_agent="Saved Search For Reddit v1.0 by /u/__py_dev")
    reddit_agent.set_oauth_app_info(client_id=CLIENT_ID,
                                    client_secret=CLIENT_SECRET,
                                    redirect_uri='http://127.0.0.1:8000/authorize_callback')
    return reddit_agent


def get_authorization_url(unauthorized_reddit_agent):
    url = unauthorized_reddit_agent.get_authorize_url(str(uuid4()), ('identity', 'edit', 'history', 'save'), True)
    return url


def get_saved_generator(authorized_reddit_agent, limit=None, time=None):
    if not time:
        time = 'all'
    return authorized_reddit_agent.user.get_saved(limit=limit, time=time)


def get_user_saved_objects(authorized_reddit_agent, limit=None, time=None):
    saved = get_saved_generator(authorized_reddit_agent, limit=limit, time=time)
    praw_name_to_objects = filter_praw_objects_to_dict(saved, ['Submission', 'Comment'])
    return praw_name_to_objects


def filter_praw_objects_to_dict(praw_object_iterable, praw_object_names_to_filter, ):
    name_to_objects_map = defaultdict(list)

    for praw_object in praw_object_iterable:
        for object_name in praw_object_names_to_filter:
            if isinstance(praw_object, PRAW_NAME_TO_OBJECT_MAP[object_name]):
                name_to_objects_map[object_name].append(praw_object)
    return name_to_objects_map


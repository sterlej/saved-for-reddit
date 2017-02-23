from pyrsistent import PClass, pmap_field, field, pmap, pvector_field, pvector, freeze, thaw

from storage.StorageLayers import PsqlStorageLayer
from datetime import datetime
import praw
from collections import defaultdict

'''
temp imports
'''
from pprint import pprint as p
from time import time as t

COMMENT_FIELDS = (('author', 'text'), ('author_flair_text', 'text'), ('created_utc', 'timestamp'),
                  ('score', 'real'), ('comment_id', 'text'), ('subreddit', 'text'), ('subreddit_id', 'text'), ('body', 'text'),
                  ('body_html', 'text'), ('link_author', 'text'), ('link_id', 'text'), ('link_title', 'text'),
                  ('link_url', 'text'), ('parent_id', 'text'))

SUBMISSION_FIELDS = (('author', 'text'), ('author_flair_text', 'text'), ('created_utc', 'timestamp'),
                     ('score', 'real'), ('submission_id', 'text'), ('subreddit', 'text'), ('subreddit_id', 'text'),
                     ('num_comments', 'real'), ('permalink', 'text'), ('title', 'text'),
                     ('url', 'text'), ('post_hint', 'text'))

PRAW_NAME_TO_OBJECT_MAP = {
    'Submission': praw.objects.Submission,
    'Comment': praw.objects.Comment
}


class RedditUser(object):
    def __init__(self, reddit_agent):
        self.reddit_agent = reddit_agent

    @property
    def user(self):
        return self.reddit_agent.user

    def get_saved_generator(self, limit=None, time=None):
        if not time:
            time = 'all'
        return self.user.get_saved(limit=limit, time=time)


def get_reddit_agent(user=None, password=None):
    reddit_agent = praw.Reddit(user_agent='praw_overflow')

    def login_reddit_agent():
        reddit_agent.login(user, password, disable_warning=True)

    if user and password:
        login_reddit_agent()
    return reddit_agent


def filter_praw_objects_to_pmap(praw_object_iterable, praw_object_names_to_filter, ):
    name_to_objects_map = defaultdict(list)

    for praw_object in praw_object_iterable:
        for object_name in praw_object_names_to_filter:
            if isinstance(praw_object, PRAW_NAME_TO_OBJECT_MAP[object_name]):
                name_to_objects_map[object_name].append(praw_object)
    return freeze(name_to_objects_map)


def get_tuple_from_dict(dictionary_object, fields_to_get, key_to_field_map=None, transform_values_func=None):
    row = [None] * len(fields_to_get)

    for key, value in dictionary_object.items():
        if key_to_field_map and key_to_field_map.get(key, None):
            key = key_to_field_map[key]
        if value and key in fields_to_get:
            if transform_values_func:
                value = transform_values_func(key, value)
            row[fields_to_get.index(key)] = value

        elif key in fields_to_get and not value:
            value = None
            row[fields_to_get.index(key)] = value
    return tuple(row)


def transform_comment_and_submission_values(field_name, value):
    if value:
        if field_name == 'subreddit':
            return value.display_name
        elif field_name == 'author':
            return value.name
        elif field_name == 'created_utc':
            return datetime.utcfromtimestamp(value).isoformat()
        else:
            return value
    else:
        return value


def get_user_saved_objects(authorized_reddit_agent, limit=None, time=None):
    r = RedditUser(reddit_agent=authorized_reddit_agent)
    gen = r.get_saved_generator(limit=limit, time=time)
    praw_name_to_objects = thaw(filter_praw_objects_to_pmap(gen, ['Submission', 'Comment']))
    return praw_name_to_objects


def main(reddit_agent):
    r = RedditUser(reddit_agent)
    gen = r.get_saved_generator(limit=5)
    comment_fields, com_types = zip(*COMMENT_FIELDS)
    submission_fields, sub_types = zip(*SUBMISSION_FIELDS)

    praw_name_to_objects = filter_praw_objects_to_pmap(gen, ['Submission', 'Comment'])
    r = r.set(saved_submissions=praw_name_to_objects['Submission'],
              saved_comments=praw_name_to_objects['Comment'])

    psql_storage = PsqlStorageLayer()
    save_row = psql_storage.save_row

    for com in r.saved_comments:
        comment_row = get_tuple_from_dict(dictionary_object=com.__dict__,
                                          fields_to_get=comment_fields,
                                          key_to_field_map={'id': 'comment_id'},
                                          transform_values_func=transform_comment_and_submission_values)

        row_to_save = comment_row
        save_row(table_name='storage_comment',
                 table_column_names_and_types=COMMENT_FIELDS,
                 value_list=row_to_save)

    for sub in r.saved_submissions:
        submission_row = get_tuple_from_dict(dictionary_object=sub.__dict__,
                                             fields_to_get=submission_fields,
                                             key_to_field_map={'id': 'submission_id'},
                                             transform_values_func=transform_comment_and_submission_values)

        row_to_save = submission_row
        save_row(table_name='storage_submission',
                 table_column_names_and_types=SUBMISSION_FIELDS,
                 value_list=row_to_save)

    psql_storage.db.disconnect()


# if __name__ == '__main__':
#     r = RedditUserAPI()
#     r.authenticate("16960711-R8qb6OM_NC9ZfxRFgDltZKWPHhM")
#     main(r.reddit_agent)

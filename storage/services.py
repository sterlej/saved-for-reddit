from reddit_saved import praw_functions


"""
When to use service

1. External service w/ model
2. Helper tasks not touching DB!!
3. Short lived obj w.o. DB state
4. Long running celery tasks

-Should be stateless
"""


def get_subset_of_dict(dictionary_obj, subset_fields_seq):
    return {k: dictionary_obj[k] for k in subset_fields_seq}


def create_model_row_from_dict(model_object, dictionary_object, id_field):
    model_row, created = model_object.objects.get_or_create(pk=dictionary_object[id_field],
                                                            defaults=dictionary_object)
    return model_row


#True service shouldn't have state, self vars in parameters
class RedditUserAPI:

    def __init__(self):
        self.reddit_agent = praw_functions.get_unauthorized_reddit_agent()
        self._authenticated = False

    def get_user_authorization_code_url(self):
        url = praw_functions.get_authorization_url(self.reddit_agent)
        return url

    def get_refresh_token(self, authorization_code):
        return self.reddit_agent.get_access_information(authorization_code)['refresh_token']

    def authenticate(self, refresh_token):
        self.reddit_agent.refresh_access_information(refresh_token)
        self._authenticated = True

    def get_praw_user(self, as_dict=False):
        if self._authenticated and as_dict:
            return self.reddit_agent.user.__dict__
        elif self._authenticated:
            return self.reddit_agent.user

    def get_profile_saved(self, limit=None, time=None):
        if self._authenticated:
            return praw_functions.get_user_saved_objects(self.reddit_agent, limit, time)






from social_django.models import UserSocialAuth
from reddit_accounts.models import LocalIdentity
from reddit_accounts.models import RedditProfile


class UserSocialService(object):
    @staticmethod
    def social_user_exists(user_social_id):
        try:
            user_social = UserSocialAuth.objects.get(uid=user_social_id)
            return True
        except UserSocialAuth.DoesNotExist:
            return False
    
    @staticmethod
    def get_social_user(user_social_id):
        try:
            user_social = UserSocialAuth.objects.get(uid=user_social_id)
        except UserSocialAuth.DoesNotExist:
            user_social= None
        return user_social
    
    @staticmethod
    def update_social_auth_refresh_token(user_social, refresh_token):
        user_social.extra_data['refresh_token'] = refresh_token
        user_social.save(update_fields=["extra_data"])

    def user_and_social_exists(self, user_social_id):
        user_social = self.get_social_user(user_social_id)
        if user_social and user_social.user_id:
            return True
        else:
            return False


def create_local_identity_and_profile(user_social):
    new_identity = LocalIdentity()
    new_identity.save()

    new_profile = RedditProfile(identity=new_identity,
                                user=user_social.user,
                                user_social=user_social)
    new_profile.save()
    return new_identity, new_profile

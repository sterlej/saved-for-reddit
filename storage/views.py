from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.generic.edit import ContextMixin
from django.views.generic import TemplateView, ListView
from uuid import uuid4

from utils.RedditAPIs import RedditUserAPI
from storage.services import  get_subset_of_dict, create_model_row_from_dict
from utils.django_functions import get_model_fields
from storage.models import Comment
from storage.models import Submission
from storage.models import RedditProfile
from storage.models import Subreddit
from storage.models import Savable
from reddit_accounts.models import LocalIdentity
from storage.upload_saved_content_to_storage import transform_comment_and_submission_values


@login_required()
def logout(request):
    logout(request)
    return redirect('home')


def authenticated(request):
    req = request.GET
    code = req['code']

    reddit_api = RedditUserAPI()
    refresh_token = reddit_api.get_access_information(code)
    refresh_token = refresh_token['refresh_token']
    reddit_api.authenticate(refresh_token)
    user_dict = reddit_api.get_praw_user(as_dict=True)
    user_id_dict = get_subset_of_dict(user_dict, ('id', 'name'))

    existing_reddit_profile = RedditProfile.objects.filter(reddit_user_id=user_id_dict['id']).first()
    if existing_reddit_profile and not request.session.get('local_id'):
        local_id = existing_reddit_profile.identity_id
    elif request.session.get('local_id'):
        local_id = request.session.get('local_id')  # Profile does not exist but local identity exists
    else:
        local_id = None  # Profile does not exist and no local id
    print(local_id, 444444444)
    if not existing_reddit_profile:
        request.session['new_profile'] = user_id_dict['id']
    profile = process_profile(user_id_dict, refresh_token, existing_reddit_profile, local_id)
    if not request.session.get('local_id') and profile:
        request.session['local_id'] = profile.identity.id  # Assign a local identity

    request.session['profile_ids'] = list(RedditProfile.objects.get_all_profiles(request.session.get('local_id')).
                                          values_list('id', flat=True))
    return redirect("home")


class UserDataMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(UserDataMixin, self).get_context_data(**kwargs)
        subreddits = sorted({savable.subreddit.name for savable in context['object_list']})
        context['subreddits'] = subreddits
        return context


class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        return context


class SavedListView(UserDataMixin, ListView):
    template_name = 'base_side_authenticated.html'
    model = Savable

    def get(self, request, *args, **kwargs):
        new_profile_id = request.session.get('new_profile')
        if new_profile_id:
            new_profile = RedditProfile.objects.get(reddit_user_id=new_profile_id)
            reddit_api = RedditUserAPI()
            reddit_api.authenticate(new_profile.refresh_token)
            get_saved_data(new_profile, reddit_api)
            del request.session['new_profile']
        return super(SavedListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        profile_ids = self.request.session.get('profile_ids')
        saved = Savable.objects.all_user_savables(profile_ids)
        return saved


def home(request):
    if not request.session.get('local_id'):
        print(1111111111)
        return HomeTemplateView.as_view()(request)
    else:
        print(22222222)
        return SavedListView.as_view()(request)


def update_profile_identities(profile, local_identity):
    profiles = RedditProfile.objects.filter(identity=profile.identity)
    local_identity = LocalIdentity.objects.get(pk=local_identity.id)

    for prof in profiles:
        prof.update_identity(local_identity)


def process_profile(user_id_dict, refresh_token, profile=None, local_id=None):
    if not local_id:
        local_identity = LocalIdentity()
        local_identity.save()
    else:
        local_identity = LocalIdentity.objects.get(pk=local_id)

    if not profile:
        profile = RedditProfile(identity=LocalIdentity.objects.get(pk=local_identity.id),
                                reddit_user_id=user_id_dict['id'],
                                username=user_id_dict['name'],
                                refresh_token=refresh_token)
        profile.save()
    elif profile.identity.id != local_identity.id:
        update_profile_identities(profile, local_identity)
    return profile


def get_saved_data(reddit_profile, reddit_saved_api):
    comment_fields = get_model_fields(Comment)
    submission_fields = get_model_fields(Submission)

    saved_praw_objects = reddit_saved_api.get_profile_saved(limit=None, time=None)

    for comment in saved_praw_objects['Comment']:
        comment_model_dict = {field: transform_comment_and_submission_values(field, value)
                              for field, value in comment.__dict__.items() if (field in comment_fields
                                                                               or field == 'id')}

        comment_model_dict['comment_id'] = comment_model_dict.pop('id')
        comment_model_dict['subreddit_id'] = comment.__dict__['subreddit_id']

        # SHOuLD NOT BE IN VIEWS
        Subreddit.objects.get_or_create(subreddit_id=comment_model_dict['subreddit_id'],
                                        name=comment_model_dict.pop('subreddit'))

        comment_obj = create_model_row_from_dict(Comment, comment_model_dict, 'comment_id')
        comment_obj.saved_by.add(reddit_profile)

    for submission in saved_praw_objects['Submission']:
        submission_model_dict = {field: transform_comment_and_submission_values(field, value)
                                 for field, value in submission.__dict__.items() if field in submission_fields
                                 or field == 'id'}

        submission_model_dict['submission_id'] = submission_model_dict.pop('id')
        submission_model_dict['subreddit_id'] = submission.__dict__['subreddit_id']
        Subreddit.objects.get_or_create(subreddit_id=submission_model_dict['subreddit_id'],
                                        name=submission_model_dict.pop('subreddit'))

        submission_obj = create_model_row_from_dict(Submission, submission_model_dict, 'submission_id')
        submission_obj.saved_by.add(reddit_profile)

from django.contrib.auth.models import User
from social_django.utils import load_strategy

strategy = load_strategy()
user = User.objects.get(pk=2)
social = user.social_auth.filter(provider='reddit')[0]
print(dir(social), "HEEREE")
social.refresh_token(strategy=strategy,
                     redirect_uri='http://localhost:8000/')
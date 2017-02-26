from ..models import RedditProfile
from .serializers import RedditProfileSerializer

from rest_framework.generics import ListAPIView, CreateAPIView


class RedditProfileListView(ListAPIView):
    serializer_class = RedditProfileSerializer
    queryset = RedditProfile.objects.all()


class RedditProfileCreateView(CreateAPIView):
    serializer_class = RedditProfileSerializer
    queryset = RedditProfile.objects.all()



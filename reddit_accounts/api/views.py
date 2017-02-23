from ..models import RedditProfile
from .serializers import RedditProfileSerializer

from rest_framework.generics import ListAPIView


class RedditProfileListView(ListAPIView):
    serializer_class = RedditProfileSerializer
    queryset = RedditProfile.objects.all()
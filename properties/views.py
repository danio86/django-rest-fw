from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Property
from .serializers import PropertySerializer


class PropertyList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in
    The perform_create method associates the post with the logged in user.
    """
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # queryset = Property.objects.annotate(
    #     likes_count=Count('likes', distinct=True),
    #     comments_count=Count('comment', distinct=True)
    # ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
        # dieser filter muss importiert und installiert werden
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        # wir sind im post model und nehmen den owner, der ist connected mit
        # einem follower über den related name in follow-model
        # von dem related name nehmen wir den owner
        # und zeigen auf dessen profile
        # Ziel: Wem folgt ein bestimmter Follower
        'likes__owner__profile',
        # hier haben wir direkte beziehungen zwischen den modellen
        # deshalb können wir bei likes abfangen, den owener nehmen und dessen
        # profil anzeigen
        # wir starten hier mit dem Modell! und enden mit dem modell
        'owner__profile',
        # wir starten beim post owner und gehen auf sein profile
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PropertyDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PropertySerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Property.objects.annotate(
        likes_count=Count('updated_at', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')

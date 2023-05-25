from django.db.models import Count
from rest_framework import generics, filters
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        # da in Follow modell zwei foreign keys sind nehmen wir den related name
        # nicht das Model
        following_count=Count('owner__following', distinct=True)
        # __ stellt die verbindung 2er Modelle her, die nicht direkt, aber
        # über das USER-Modell verbunden sind.
        # Da wir mehr als ein Feld innerhalb der annotate-Funktion definieren
        # werden, müssen wir hier auch distinct=True übergeben, um nur die
        # unique Beiträge zu zählen. Ohne dies würden wir Duplikate erhalten.

        # die drei müssen auch in den styrealizer!
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
        # created_at ist so attached to followed/ing, also zu anderen
        # attributen im selben model und zu owner (anderes Model)
    ]
    # Als Nächstes müssen wir unsere Filter erstellen. Um diese Felder
    # sortierbar zu machen, werde ich das Attribut filter_backends auf
    # OrderingFilter setzen. Außerdem muss ich die ordering_fields auf die
    # Felder setzen, die wir gerade annotiert haben, nämlich die Anzahl der
    # Beiträge, Follower und Personen, denen gefolgt wird.

    # Die annotate-Funktion ermöglicht es uns, zusätzliche Felder zu definieren
    # die dem Queryset hinzugefügt werden sollen. In unserem Fall werden wir
    # Felder hinzufügen, um herauszufinden, wie viele Beiträge und Follower ein
    # Benutzer hat und wie vielen anderen Benutzern sie folgen.


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    # queryset ist nur von ober koppiert um die neu erstellten Felder auch
    # in einem einzelnen Profil zu sehen.
    serializer_class = ProfileSerializer

# from rest_framework import generics
# from drf_api.permissions import IsOwnerOrReadOnly
# from .models import Profile
# from .serializers import ProfileSerializer


# class ProfileList(generics.ListAPIView):
#     """
#     List all profiles.
#     No create view as profile creation is handled by django signals.
#     """
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


# class ProfileDetail(generics.RetrieveUpdateAPIView):
#     """
#     Retrieve or update a profile if you're the owner.
#     """
#     permission_classes = [IsOwnerOrReadOnly]
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


# from django.http import Http404
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Profile
# from .serializers import ProfileSerializer
# from drf_api.permissions import IsOwnerOrReadOnly


# class ProfileList(APIView):
#     """
#     List all profiles
#     No Create view (post method), as profile creation handled by django signals
#     """

#     def get(self, request):
#         profiles = Profile.objects.all()
#         serializer = ProfileSerializer(
#             profiles, many=True, context={'request': request}
#         )
#         return Response(serializer.data)


# class ProfileDetail(APIView):
#     serializer_class = ProfileSerializer
#     permission_classes = [IsOwnerOrReadOnly]

#     def get_object(self, pk):
#         try:
#             profile = Profile.objects.get(pk=pk)
#             self.check_object_permissions(self.request, profile)
#             return profile
#         except Profile.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(
#             profile, context={'request': request}
#         )
#         return Response(serializer.data)

#     def put(self, request, pk):
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(
#             profile, data=request.data, context={'request': request}
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

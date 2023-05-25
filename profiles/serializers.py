from followers.models import Follower
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    # das fügt ein weiters api feld hinzu
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
        # checkt user ownership.
        # Die Argumente müssen über views mitgeliefert werden.

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
                # checks if the loggedin user is following this profile
            ).first()
            # print(following, 'test')
            # das gergibt das ana dan folgt oder none
            return following.id if following else None
        return None
        # dieser Block checkt on der user einen autentifizierten Follower hat.

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count',
        ]

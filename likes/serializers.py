from rest_framework import serializers
from posts.models import Like


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Like
        fields = [
            'id', 'owner', 'post', 'created_at'
        ]

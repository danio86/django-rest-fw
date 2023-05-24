from rest_framework import serializers
from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    # def validate_image(self, value):
    #     if value.size > 2 * 1024 * 1024:
    #         raise serializers.ValidationError('Image size larger than 2MB!')
    #     if value.image.height > 4096:
    #         raise serializers.ValidationError(
    #             'Image height larger than 4096px!'
    #         )
    #     if value.image.width > 4096:
    #         raise serializers.ValidationError(
    #             'Image width larger than 4096px!'
    #         )
    #     return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'post', 'content'
        ]


class CommentDetailSerializer(CommentSerializer):


"""
Serializer for the Comment model used in Detail view
Post is a read only field so that we dont have to set it on each update
"""
post = serializers.ReadOnlyField(source='post.id')
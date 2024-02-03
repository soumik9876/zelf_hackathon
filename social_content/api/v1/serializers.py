from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from social_content.models import OriginDetails, AuthorInfo, Context, Media, ContentStats, AuthorStats, Author, Content


class OriginDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OriginDetails
        exclude = ['id']


class ContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Context
        exclude = ['id']


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        exclude = ['id']


class ContentStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentStats
        exclude = ['id']


class AuthorStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorStats
        exclude = ['id']


class AuthorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorInfo
        exclude = ['id']


class AuthorSerializer(WritableNestedModelSerializer):
    info = AuthorInfoSerializer(required=False)
    stats = AuthorStatsSerializer(required=False)

    class Meta:
        model = Author
        exclude = ['id']


class ContentSerializer(WritableNestedModelSerializer):
    author_details = AuthorSerializer(read_only=True, source='author')
    context = ContextSerializer(required=False)
    origin_details = OriginDetailsSerializer(required=False)
    media = MediaSerializer(required=False)
    stats = ContentStatsSerializer(required=False)

    class Meta:
        model = Content
        exclude = ['id']

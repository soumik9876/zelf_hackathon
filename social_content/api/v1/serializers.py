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


class AuthorSerializer(serializers.ModelSerializer):
    info = AuthorInfoSerializer()
    stats = AuthorStatsSerializer()

    class Meta:
        model = Author
        exclude = ['id']


class ContentSerializer(serializers.ModelSerializer):
    author_details = AuthorSerializer(read_only=True, source='author')
    context = ContextSerializer()
    origin_details = OriginDetailsSerializer()
    media = MediaSerializer()
    stats = ContentStatsSerializer()

    class Meta:
        model = Content
        exclude = ['id']

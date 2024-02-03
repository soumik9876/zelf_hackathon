from django.db.models import Manager

from social_content.models import Author


class ContentManager(Manager):
    def create_or_update_from_response(self, response):
        contents = response.get('data')
        for content in contents:
            """
                We iterate through the content list response, get author data, then create content in DB
            """
            author = content.get('author')
            author_obj = Author.objects.create_or_update_author_from_data(data=author)

            content_data = {
                'hack_uid': content.get('unique_id'),
                'originally_created_at': content.get('creation_info').get('created_at'),
                'context': content.get('context'),
                'origin_details': content.get('origin_details'),
                'media': content.get('media'),
                'stats': self.get_stats(stats=content.get('stats')),
                'author': author_obj.id
            }
            from social_content.api.v1.serializers import ContentSerializer
            from social_content.models import Content
            """
                Depending on the existence of the content in DB, we create or update it
            """
            content_obj = Content.objects.filter(hack_uid=content_data.get('hack_uid')).first()
            if content_obj is None:
                serializer = ContentSerializer(data=content_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                serializer = ContentSerializer(instance=content_obj, data=content_data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

    def get_stats(self, stats):
        digg_counts = stats.get('digg_counts')
        return {
            'likes': digg_counts.get('likes').get('count'),
            'views': digg_counts.get('views').get('count'),
            'comments': digg_counts.get('comments').get('count'),
        }

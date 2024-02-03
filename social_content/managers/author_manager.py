import datetime

from django.db.models import Manager
from django.utils import timezone

from social_content.clients.hackapi_client import HackAPIClient


class AuthorManager(Manager):
    def create_or_update_author_from_data(self, data):
        """
            data format:
            {
                "id": 302048,
                "username": "sephora"
            }
        """
        hack_uid = data.get('id')
        from social_content.api.v1.serializers import AuthorSerializer
        from social_content.models import Author
        author_obj: Author = Author.objects.filter(hack_uid=hack_uid).first()
        max_last_mod_limit = timezone.now() - datetime.timedelta(minutes=5)
        """
            We only try to call the author API if the author does not exist in the DB or if exists, it was modified more than
            5 minutes ago. This way we can save API calls for duplicate authors.
        """
        if author_obj is None or author_obj.modified_date < max_last_mod_limit:
            client = HackAPIClient()
            response = client.get_author_data(uid=hack_uid)
            if response.status_code >= 400:
                """
                    In this case we just keep the passed data
                """
                print('Author data get error')
            else:
                data = response.json()

        if author_obj is None:
            serializer = AuthorSerializer(data=data)
            serializer.is_valid()
            obj = serializer.save()
        else:
            serializer = AuthorSerializer(instance=author_obj, data=data, partial=True)
            serializer.is_valid()
            obj = serializer.save()

        return obj

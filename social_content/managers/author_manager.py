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
        author_data = {
            'hack_uid': data.get('id'),
            'username': data.get('username')
        }
        """
            We only try to call the author API if the author does not exist in the DB or if exists, it was modified more than
            5 minutes ago. This way we can save API calls for duplicate authors.
        """
        if author_obj is None or author_obj.modified_date < max_last_mod_limit:
            client = HackAPIClient()
            response = client.get_author_data(uid=hack_uid)
            print(response.json(), response.status_code)
            if response.status_code >= 400:
                """
                    In this case we just keep the passed data
                """
                print('Author data get error')
            else:
                data = response.json().get('data')
                if len(data) > 0:
                    author_data.update({
                        'hack_uid': data[0].get('unique_id'),
                        'stats': {
                            'followers': data[0].get('stats').get('digg_count').get('followers').get('count')
                        }
                    })
        """
            Depending on the existence of the content in DB, we create or update it
        """
        if author_obj is None:
            serializer = AuthorSerializer(data=author_data)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
        else:
            serializer = AuthorSerializer(instance=author_obj, data=author_data, partial=True)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()

        return obj

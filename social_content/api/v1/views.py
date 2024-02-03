from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response

from core.api.paginations import StandardResultsSetPagination
from core.utils import get_logger
from social_content.api.v1.serializers import ContentSerializer
from social_content.clients.hackapi_client import HackAPIClient
from social_content.models import Content

logger = get_logger()


class ContentAuthorAPIView(ListAPIView):
    serializer_class = ContentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
            At first, we call the 3rd party content API according to request page number. We update or create the
            content data in our own db, we also fetch author data conditionally and update them to DB. Finally we
            serve the content and author data from our DB
        """
        page = self.request.query_params.get('page', 1)
        # queryset = self.filter_queryset(self.get_queryset())
        client = HackAPIClient()
        try:
            """
                Everytime we are trying to get new content data from third party API since content data might get 
                updated frequently
            """
            contents = client.get_content_data(page=page)
            Content.objects.create_or_update_from_response(response=contents.json())
        except Exception as e:
            logger.error(f'Error getting content: {e}')

        return Content.objects.all()
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        #
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)

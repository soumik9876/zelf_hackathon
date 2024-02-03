from django.db.models import Avg, Max, Count
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

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
            content data in our own db, we also fetch author data conditionally and update them to DB. Finally, we
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


class StatsDataAPIView(APIView):
    def get(self, request, *args, **kwargs):
        aggregates = Content.objects.aggregate(
            Avg('stats__likes'),
            Avg('stats__views'),
            Avg('stats__comments'),
            Max('stats__likes'),
            Max('stats__views'),
            Max('stats__comments'),
            Max('author__stats__followers')
        )

        aggregate_map = {
            'avg_likes': 'stats__likes__avg',
            'avg_views': 'stats__views__avg',
            'avg_comments': 'stats__comments__avg',
            'max_likes': 'stats__likes__max',
            'max_views': 'stats__views__max',
            'max_comments': 'stats__comments__max',
            'most_followed': 'author__stats__followers__max'
        }
        response = {key: aggregates[value] for key, value in aggregate_map.items()}

        most_popular_platform = Content.objects.values_list('origin_details__origin_platform') \
            .annotate(cnt=Count('origin_details__origin_platform')).order_by('-cnt').first()
        if most_popular_platform is not None:
            response.update({
                'most_popular_platform': {
                    'name': most_popular_platform[0],
                    'post_count': most_popular_platform[1]
                }
            })

        return Response(response)


class ContentByDate(APIView):
    def get(self, request, *args, **kwargs):
        content_by_date = Content.objects.values('originally_created_at').annotate(
            cnt=Count('originally_created_at')).order_by('originally_created_at')

        return Response(content_by_date)


class ContentByPlatform(APIView):
    def get(self, request, *args, **kwargs):
        content_by_platform = Content.objects.values('origin_details__origin_platform').annotate(
            cnt=Count('origin_details__origin_platform')).order_by('origin_details__origin_platform')

        return Response(content_by_platform)

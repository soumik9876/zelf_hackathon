import requests

from zelf_hackathon.settings import env


class HackAPIClient:
    """
        This class will handle the data fetching functionalities from hackapi
    """

    def get_headers(self):
        return {
            'x-api-key': env.str('HACK_API_KEY')
        }

    def get_content_data(self, page=1):
        request_url = f'https://hackapi.hellozelf.com/backend/api/v1/contents?page={page}'
        response = requests.get(request_url, headers=self.get_headers())
        return response

    def get_author_data(self, uid):
        request_url = f'https://hackapi.hellozelf.com/backend/api/v1/authors/{uid}'
        response = requests.get(request_url, headers=self.get_headers())
        return response

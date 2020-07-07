from requests import get
from requests.exceptions import RequestException
from contextlib import closing


def is_valid_response(response):
    """
    Returns true if the response is valid, false if not
    :param response: response to validate
    :return: bool
    """
    content_type = response.headers['Content-Type'].lower()
    return (response.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


class Requester:
    __url = ''

    def __init__(self, url=''):
        self.__url = url

    def get_page_content(self):
        """
        Attempts to fetch the content of the provided web page by making
        use of the GET method, the response will typically be an HTML/XML text
        document. If nothing is found None will be returned.
        :return: website content
        """
        try:
            with closing(get(self.__url, stream=True)) as response:
                if is_valid_response(response):
                    return response.content
                else:
                    return None
        except RequestException as err:
            print(f"Error during get request {err}")
            return None

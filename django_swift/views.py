import logging
from django.core.files.storage import default_storage
from django.http.response import StreamingHttpResponse, HttpResponse


logger = logging.getLogger()
ACCEPT_HEADERS = ['Accept', 'Accept-Encoding', 'Accept-Language', 'Range']


def download(request, name):
    try:
        request_headers = {}
        for key in ACCEPT_HEADERS:
            meta_key = key.replace('-', '_').upper()
            if meta_key in request.META:
                request_headers[key] = request.META[meta_key]
        f = default_storage.open(name)
        headers, data = f.connection.get_object(
            f.container_name,
            f.name,
            resp_chunk_size=1024 * 1024,
            headers=request_headers
        )
        response = StreamingHttpResponse(data)
        for item in headers.viewitems():
            response[item[0]] = item[1]
    except BaseException as e:
        response = HttpResponse()
        if hasattr(e, 'http_status'):
            response.status_code = e.http_status
        else:
            response.status_code = 500
            logger.exception(e)
    return response

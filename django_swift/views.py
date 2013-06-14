import logging
from django.core.files.storage import default_storage
from django.http.response import StreamingHttpResponse, HttpResponse


logger = logging.getLogger()

def download(request, name):
    try:
        f = default_storage.open(name)
        headers, data = f.connection.get_object(
            f.container_name,
            f.name,
            resp_chunk_size = 1024 * 1024
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
    

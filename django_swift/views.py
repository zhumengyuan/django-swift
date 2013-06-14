import logging
from django.core.files.storage import default_storage
from django.http.response import StreamingHttpResponse, HttpResponse


logger = logging.getLogger()

def download(request, name):
    try:
        f = default_storage.open(name)
        head, data = f.connection.get_object(
            f.container_name,
            f.name,
            resp_chunk_size = 1024 * 1024
        )
        return StreamingHttpResponse(data, head)
    except BaseException as e:
        response = HttpResponse()   
        if hasattr(e, 'http_status'):
            response.status_code = e.http_status
        else:
            response.status_code = 500
            logger.exception(e)
    return response
    

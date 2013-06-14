import logging
from django.core.files.storage import default_storage
from django.http.response import StreamingHttpResponse, HttpResponse


logger = logging.getLogger()

def download(request, name):
    try:
        f = default_storage.open(name)
        return StreamingHttpResponse(iter(f))
    except BaseException as e:
        response = HttpResponse()   
        if hasattr(e, 'http_status'):
            response.status_code = e.http_status
        else:
            response.status_code = 500
            logger.exception(e)
    return response
    

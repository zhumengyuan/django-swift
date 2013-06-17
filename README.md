django_swift
============

django_swift is a storage backend for django

django setings.py demo
============
* DEFAULT_FILE_STORAGE = 'django_swift.storage.SwiftStorage'
* SWIFT_AUTHURL = 'http://10.1.50.1:8080/auth/v1.0'
* SWIFT_USER = 'root'
* SWIFT_KEY = 'system:pass'
* SWIFT_CONTAINER_NAME = 'container name'
* SWIFT_RETRIES = 5
* SWIFT_PREAUTHURL = None
* SWIFT_PREAUTHTOKEN = None
* SWIFT_SNET = False
* SWIFT_STARTING_BACKOFF = 1
* SWIFT_TENANT_NAME = None
* SWIFT_OS_OPTIONS = None
* SWIFT_AUTH_VERSION = "1"
* SWIFT_CACERT = None
* SWIFT_INSECURE = False

django url settings
====================
* set in url.py: url('^media/([\w|.|/]+)', "django_swift.views.download")
* set in settings.py: MEDIA_URL = '/media/'

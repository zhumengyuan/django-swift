#encoding:utf-8
import swiftclient
from django.conf import settings
from django.core.files.storage import Storage
from django.core.files.base import File


class SwiftclientStorageFile(File):

    def __init__(self, connection, container_name, name, *args, **kwargs):
        self.connection = connection
        self.container_name = container_name
        self._pos = 0
        File.__init__(
            self,
            file=None,
            name=name,
            *args,
            **kwargs
        )

    def size(self):
        try:
            head = self.connection.head_object(
                self.container_name,
                self.name,
            )
            return int(head['content-length'])
        except BaseException:
            return 0


    def read(self, chunk_size=-1):
        """
        Reads specified chunk_size or the whole file if chunk_size is None.
        """
        if self._pos == self.size() or chunk_size == 0:
            return ""

        if chunk_size < 0:
            _, data = self.connection.get_object(
                self.container_name,
                self.name,
            )
        else:
            _, data = self.connection.get_object(
                self.container_name,
                self.name,
                resp_chunk_size=chunk_size
            )
        self._pos += len(data)
        return data

    def open(self, *args, **kwargs):
        """
        Opens the cloud file object.
        """
        self._pos = 0

    def close(self, *args, **kwargs):
        self._pos = 0

    @property
    def closed(self):
        return not hasattr(self, "_file")

    def seek(self, pos):
        self._pos = pos


class SwiftStorage(Storage):

    authurl = getattr(settings, 'SWIFT_AUTHURL', None)
    user = getattr(settings, 'SWIFT_USER', None)
    key = getattr(settings, 'SWIFT_KEY', None)
    container_name = getattr(settings, 'SWIFT_CONTAINER_NAME', None)
    retries = getattr(settings, 'SWIFT_RETRIES', 5)
    preauthurl = getattr(settings, 'SWIFT_PREAUTHURL', None)
    preauthtoken = getattr(settings, 'SWIFT_PREAUTHTOKEN', None)
    snet = getattr(settings, 'SWIFT_SNET', False)
    starting_backoff = getattr(settings, 'SWIFT_STARTING_BACKOFF', 1)
    tenant_name = getattr(settings, 'SWIFT_TENANT_NAME', None)
    os_options = getattr(settings, 'SWIFT_OS_OPTIONS', None)
    auth_version = getattr(settings, 'SWIFT_AUTH_VERSION', "1")
    cacert = getattr(settings, 'SWIFT_CACERT', None)
    insecure = getattr(settings, 'SWIFT_INSECURE', False)


    def __init__(self, location=None, base_url=None):
        self._connection = None
        if location is None:
            location = settings.MEDIA_ROOT
        self.location = location
        if base_url is None:
            base_url = settings.MEDIA_URL
        self.base_url = base_url

    @property
    def connection(self):
        if self._connection is None:
            self._connection = swiftclient.Connection(
                authurl = self.authurl,
                user = self.user,
                key = self.key,
                retries = self.retries,
                preauthurl = self.preauthurl,
                preauthtoken = self.preauthurl,
                snet = self.snet,
                starting_backoff = self.starting_backoff,
                tenant_name = self.tenant_name,
                os_options = self.os_options,
                auth_version = self.auth_version,
                cacert = self.cacert,
                insecure = self.insecure,
            )
        return self._connection

    def _open(self, name, mode):
        return SwiftclientStorageFile(
            self.connection,
            self.container_name,
            name,
        )

    def _save(self, name, content):
        self.connection.put_object(
            self.container_name,
            name,
            content
        )
        return name

    def delete(self, name):
        self.connection.delete_object(
            self.container_name,
            name
        )
    
    def exists(self, name):
        try:
            self.connection.head_object(
                self.container_name,
                name
            )
            return True
        except BaseException:
            return False

    def size(self, name):
        try:
            head = self.connection.head_object(
                self.container_name,
                name
            )
            return int(head['content-length'])
        except BaseException:
            return 0
    
    def url(self, name):
        """
        Returns an absolute URL where the content of each file can be
        accessed directly by a web browser.
        """
        return "{0}/{1}".format(self.base_url, name)

    def listdir(self, path):
        """
        Lists the contents of the specified path, returning a 2-tuple;
        the first being an empty list of directories (not available
        for quick-listing), the second being a list of filenames.

        If the list of directories is required, use the full_listdir method.
        """
        files = []
        if path and not path.endswith("/"):
            path = "{0}/".format(path)
        path_len = len(path)
        for name in [x["name"] for x in
                     self.connection.get_container(self.container_name, full_listing=True)[1]]:
            files.append(name[path_len:])
        return ([], files)

    def full_listdir(self, path):
        """
        Lists the contents of the specified path, returning a 2-tuple
        of lists; the first item being directories, the second item
        being files.
        """
        dirs = set()
        files = []
        if path and not path.endswith("/"):
            path = "{0}/".format(path)
        path_len = len(path)
        for name in [x["name"] for x in
                     self.connection.get_container(self.container_name, full_listing=True)[1]]:
            name = name[path_len:]
            slash = name[1:-1].find("/") + 1
            if slash:
                dirs.add(name[:slash])
            elif name:
                files.append(name)
        dirs = list(dirs)
        dirs.sort()
        return (dirs, files)



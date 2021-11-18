################################################################################
# Based on this pr https://github.com/JacekPliszka/PyGithub/pull/1/files
# which adds the artifact fetching
import os
import requests, zipfile, io
from pathlib import Path
import github.GithubObject


class Artifact(github.GithubObject.CompletableGithubObject):
    """
    This class represents Artifacts.
    The reference can be found here https://developer.github.com/v3/actions/artifacts/
    """

    def __repr__(self):
        return self.get__repr__({"name": self._name.value})

    @property
    def id(self):
        """
        :type: integer
        """
        self._completeIfNotSet(self._id)
        return self._id.value

    @property
    def node_id(self):
        """
        :type: string
        """
        self._completeIfNotSet(self._node_id)
        return self._node_id.value

    @property
    def name(self):
        """
        :type: string
        """
        self._completeIfNotSet(self._name)
        return self._name.value

    @property
    def size_in_bytes(self):
        """
        :type: int
        """
        self._completeIfNotSet(self._size_in_bytes)
        return self._size_in_bytes.value

    @property
    def url(self):
        """
        :type: string
        """
        self._completeIfNotSet(self._url)
        return self._url.value

    @property
    def archive_download_url(self):
        """
        :type: string
        """
        self._completeIfNotSet(self._archive_download_url)
        return self._archive_download_url.value

    @property
    def expired(self):
        """
        :type: bool
        """
        self._completeIfNotSet(self._expired)
        return self._expired.value

    @property
    def created_at(self):
        """
        :type: datetime.datetime
        """
        self._completeIfNotSet(self._created_at)
        return self._created_at.value

    @property
    def expires_at(self):
        """
        :type: datetime.datetime
        """
        self._completeIfNotSet(self._expires_at)
        return self._expires_at.value

    @property
    def updated_at(self):
        """
        :type: datetime.datetime
        """
        self._completeIfNotSet(self._updated_at)
        return self._updated_at.value



    def _initAttributes(self):
        self._id = github.GithubObject.NotSet
        self._node_id = github.GithubObject.NotSet
        self._name = github.GithubObject.NotSet
        self._size_in_bytes = github.GithubObject.NotSet
        self._url = github.GithubObject.NotSet
        self._archive_download_url = github.GithubObject.NotSet
        self._expired = github.GithubObject.NotSet
        self._created_at = github.GithubObject.NotSet
        self._expires_at = github.GithubObject.NotSet
        self._updated_at = github.GithubObject.NotSet
        self._artifact = github.GithubObject.NotSet

    def download(self, destination_directory:str, headers:dict):
        destination_directory = Path( os.path.dirname(destination_directory) ).resolve()
        os.makedirs(destination_directory, exist_ok=True)

        r = requests.get(self.archive_download_url, headers=headers)
        if r.status_code == 200:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(destination_directory)
            return destination_directory
        return None


    def _useAttributes(self, attributes):
        if "id" in attributes:
            self._id = self._makeIntAttribute(attributes["id"])
        if "node_id" in attributes:
            self._node_id = self._makeStringAttribute(attributes["node_id"])
        if "name" in attributes:
            self._name = self._makeStringAttribute(attributes["name"])
        if "size_in_bytes" in attributes:
            self._size_in_bytes = self._makeIntAttribute(attributes["size_in_bytes"])
        if "url" in attributes:
            self._url = self._makeStringAttribute(attributes["url"])
        if "archive_download_url" in attributes:
            self._archive_download_url = self._makeStringAttribute(attributes["archive_download_url"])
        if "expired" in attributes:
            self._expired = self._makeBoolAttribute(attributes["expired"])
        if "created_at" in attributes:
            self._created_at = self._makeDatetimeAttribute(attributes["created_at"])
        if "expires_at" in attributes:
            self._expires_at = self._makeDatetimeAttribute(attributes["expires_at"])
        if "updated_at" in attributes:
            self._updated_at = self._makeDatetimeAttribute(attributes["updated_at"])

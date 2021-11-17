import github.GithubObject
import github.PaginatedList
import github.Repository
from .Artifact import Artifact
from pprint import pp

def get_artifacts(self):
    """
    :calls: `GET /repos/:owner/:repo/actions/artifacts
        <https://developer.github.com/v3/actions/artifacts/#list-artifacts-for-a-repository>
    :rtype: :class:`github.PaginatedList.PaginatedList` of :class:`github.Artifacts.Artifact`
    """

    return github.PaginatedList.PaginatedList(
        Artifact,
        self._requester,
        self.url + "/actions/artifacts",
        None,
        list_item="artifacts",
    )


def artifact_getter(r:github.Repository) -> github.PaginatedList.PaginatedList:
    r.get_artifacts = get_artifacts.__get__(r)
    return r.get_artifacts()

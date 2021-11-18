from github.PaginatedList import PaginatedList
from out import out
from .Artifact import Artifact
from .rate_limiter import rate_limiter


def download_latest_artifact(
    self,
    directory:str,
    headers:dict,
    named:str = "repository-scan-result") -> str:
    """
    """
    out.log(f"Looking for latest artifact matching [{named}]")
    artifact = self.get_latest_artifact(named)
    if artifact != None:
        return artifact.download(f"{directory}/{self.name}/", headers)
    return None

def get_latest_artifact(self, named:str = "repository-scan-result") -> Artifact:
    """
    Gets all artifacts for this repoistory and finds the first one with a
    name that matches named
    """
    rate_limiter.check()
    artifacts = self.get_artifacts()
    total:int = artifacts.totalCount
    out.log(f"Repository [{self.name}] has [{total}] artifacts. Looking for [{named}]")
    i:int = 0
    for a in artifacts:
        i = i + 1
        out.debug(f"Artifact [{i}/{total}] named [{a.name}] updated at [{a.updated_at}]")
        if a.name == named:
            out.debug(f"Artifact found [{a.name}] [{a.node_id}]")
            return a
        rate_limiter.check()
    return None


def get_artifacts(self):
    """
    :calls: `GET /repos/:owner/:repo/actions/artifacts
        <https://developer.github.com/v3/actions/artifacts/#list-artifacts-for-a-repository>
    :rtype: :class:`github.PaginatedList.PaginatedList` of :class:`github.Artifacts.Artifact`
    """

    return PaginatedList(
        Artifact,
        self._requester,
        self.url + "/actions/artifacts",
        None,
        list_item="artifacts",
    )

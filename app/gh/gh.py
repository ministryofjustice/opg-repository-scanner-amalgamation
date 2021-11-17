from github import Github
from github.Organization import Organization
from github.Team import Team
from github.Repository import Repository
from github.PaginatedList import PaginatedList

from out import out
from gh.ratelimit import limiter
from gh.artifacts.Artifact import Artifact
from gh.artifacts.get import artifact_getter
from files.write import *
from pprint import pp
# github base helper class
class gh:
    """
    Github helper class
    Uses the ratelimit library with sleep and retry for most functions

    """
    def connection(self, token:str) -> Github:
        """
        Create a github connection authenticated with the token provided.
        Note: Does not call the rate limiter
        """
        out.log("Connecting to github via token auth")
        return Github(token)

    def organization(self, connection:Github, slug:str) -> Organization:
        """
        Find and return the organization from the githbu connection using the slug.

        Does a rate limiter check.
        """
        limiter.check(connection)
        out.log(f"Getting organization [{slug}]")
        return connection.get_organization(slug)

    def team(self, connection:Github, organization:Organization, slug:str) -> Team:
        """
        Fetches a team from the organization matching the slug passed.

        Does a rate limiter check
        """
        limiter.check(connection)
        out.log(f"Getting team by slug [{slug}] from organization [{organization.name}]")
        return organization.get_team_by_slug(slug)

    def repositories(self, connection:Github, team:Team):
        """
        Finds all repositories for the team passed and returns them

        Uses rate limiter
        """
        limiter.check(connection)
        out.log(f"Getting repositories for team [{team.slug}]")

        return team.get_repos()

    def artifacts(self, connection:Github, repository:Repository) -> PaginatedList:
        """
        Method to fetch all artifacts created by workflows within the
        repository passed
        """
        limiter.check(connection)
        out.log(f"Getting artifacts for [{repository.name}]")
        return artifact_getter(repository)

    def artifact_for_reports(self, connection:Github, repository:Repository, seaarch_for:str = "repository-scan-result") -> Artifact:
        """
        Find all artifacts for this repository (as the list is paginated), look
        for the first (as result sorted by date) that matches the search_for
        param and return that
        """

        artifacts = self.artifacts(connection, repository)
        for a in artifacts:
            limiter.check(connection)
            out.debug(f"Artifact [{a.name}] on [{a.updated_at}]")
            if seaarch_for == a.name:
                out.debug(f"Found artifact [{a.name}] with node id [{a.node_id}]")
                return a
        return None

    def download_artifact(self, artifact:Artifact, directory:str, token:str):
        """
        Download the zip from the artifact data, use the token in the auth
        headers and then extract the zip to directory
        """
        url = artifact.archive_download_url
        out.debug(f"Downloading artifact from [{url}]")
        headers = {'Authorization': f"token {token}"}
        return write.zip_to_file(url, directory, headers)

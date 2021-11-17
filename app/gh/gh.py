from github import Github
from github.Organization import Organization
from github.Team import Team
from github.Repository import Repository
from github.PaginatedList import PaginatedList
from gh.ratelimit import limiter
from out import out
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

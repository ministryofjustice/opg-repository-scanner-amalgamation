from github import Repository
from .Repository import get_artifacts, get_latest_artifact

def add_repository_extensions(repository:Repository):
    """
    As PyHub currently doesnt support repo->artifact api endpoints
    these functions provide that capability, so push them on to
    the instance

    Also add custom function to find the specific artifact we want
    """
    repository.get_artifacts = get_artifacts.__get__(repository)
    repository.get_latest_artifact = get_latest_artifact.__get__(repository)

    return repository

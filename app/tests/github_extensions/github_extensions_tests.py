from github.PaginatedList import T
from github.Repository import Repository
from pprint import pp
import pytest
import types
from github_extensions.github_extensions import add_repository_extensions


def test_github_extensions_add_repository_extensions():
    """
    Check the custom methods we add to a repository reports as a method
    correctly
    """
    r = Repository(None, None, {'name':'Test'}, False)
    r = add_repository_extensions(r)

    is_method = hasattr(r, 'get_artifacts') and type(getattr(r, 'get_artifacts')) == types.MethodType
    assert is_method == True

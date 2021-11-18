import pytest
from github_extensions.Artifact import Artifact


def test_artifact_type():
    a = Artifact(None, None, {}, False)
    assert type(a) == Artifact

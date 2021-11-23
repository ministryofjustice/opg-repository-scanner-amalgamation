import os
import pytest
from pprint import pp
from main import timestamp_directory, merge_raw_packages, packages_to_html, reduce_packages
from pathlib import Path

_ROOT_DIR = Path( os.path.dirname(__file__ ) + "/../../" ).resolve()

def test_timestamp_directory():
    """
    Make sure dir is created and contains __downloads__
    """
    standard = str(timestamp_directory())

    assert ("__downloads__" in standard) == True
    assert os.path.isdir(standard)


def test_merge_raw_packages():
    """
    """
    dir = Path( os.path.dirname(__file__ ) + "/../../" ).resolve()
    # add the same data in multiple times to ensure duplicates are removed
    files = [
        ("OLD", f"{_ROOT_DIR}/__samples/raw_files/old"),
        ("NEW", f"{_ROOT_DIR}/__samples/raw_files/new"),
        ("NEW", f"{_ROOT_DIR}/__samples/raw_files/new"),
        ("NEW", f"{_ROOT_DIR}/__samples/raw_files/new")
    ]

    all = merge_raw_packages(files)
    # 10 packages in the new, 20 in old, 1 exact duplicate
    assert len(all) == 29


def test_reduce_packages():
    """
    """
    packages = [
        {'name': "pkg1", 'version': '==1.0', 'repository': 'test', 'source': '1'},
        {'name': "pkg1", 'version': '==1.1', 'repository': 'test', 'source': '1'},
        {'name': "pkg1", 'version': '==1.2', 'repository': 'test', 'source': '1'},

        {'name': "pkg1", 'version': '==1.3', 'repository': 'test', 'source': '2'},

        {'name': "pkg2", 'version': '==1.0', 'repository': 'test', 'source': '1'}

    ]

    reduced = reduce_packages(packages)
    pkg1s = list( filter ( lambda p: p['name'] == 'pkg1', reduced))
    pkg1s2 = list( filter ( lambda p: p['source'] == '2', pkg1s))

    assert len(reduced) == 3
    assert len(pkg1s) == 2

    assert len(pkg1s2) == 1
    pkg = pkg1s2.pop()
    assert pkg.get('source') == '2'


def test_packages_to_html():
    """
    """
    files = [
        ("OLD", f"{_ROOT_DIR}/__samples/raw_files/old"),
        ("NEW", f"{_ROOT_DIR}/__samples/raw_files/new")
    ]
    all = merge_raw_packages(files)
    html_f, json_f = packages_to_html(all)

    assert os.path.isfile(html_f)
    assert os.path.isfile(json_f)

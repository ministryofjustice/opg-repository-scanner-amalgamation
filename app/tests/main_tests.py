import os
import pytest
from pprint import pp
from main import timestamp_directory, merge_raw_packages, packages_to_html
from pathlib import Path

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
    files = [
        ("OLD", f"{dir}/__samples/raw_files/old"),
        ("NEW", f"{dir}/__samples/raw_files/new")
    ]

    all = merge_raw_packages(files)
    assert len(all) == 30


def test_packages_to_html():
    """
    """
    dir = Path( os.path.dirname(__file__ ) + "/../../" ).resolve()
    files = [
        ("OLD", f"{dir}/__samples/raw_files/old"),
        ("NEW", f"{dir}/__samples/raw_files/new")
    ]
    all = merge_raw_packages(files)
    html_f, json_f = packages_to_html(all)

    assert os.path.isfile(html_f)
    assert os.path.isfile(json_f)

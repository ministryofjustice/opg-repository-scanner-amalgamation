#!/usr/bin/env python
import os
from pathlib import Path
from datetime import datetime
from argparse import Namespace
from pprint import pp

from github import Repository
from github.MainClass import Github
from github.Organization import Organization
from gh import gh
from inputs.handler import handler
from out import out


def github_info(args:Namespace) -> dict:
    """
    Get all the github info setup and return a dict of data
    """
    g = gh()
    connection = g.connection(args.organisation_token)
    org = g.organization(connection, args.organisation_slug)
    team = g.team(connection, org, args.team_slug)
    return {
        'g': g,
        'connection': connection,
        'org': org,
        'team': team,
        'repos': g.repositories(connection, team)
    }


def download_artifact(repo:Repository.Repository, g:gh, connection, token:str, dir:str) -> str:
    """
    Using data from the repo fetch, download and extract relevant artifacts

    Return the folder locations extracted to, or None
    """

    res = g.artifact_for_reports(connection, repo)
    if res == None:
        out.notice(f"Cannot find artifact for [{repo.name}]", "Artifact missing")
    else:
        out.log("Downloading artifact")
        dl = g.download_artifact(res, f"{dir}/{repo.name}/", token)
        if dl == None:
            out.warning(
                f"Artifact [{res.name}, {res.node_id}] for repo [{repo.name}] from [{res.archive_download_url}]",
                "Artifact download failure"
            )
        else:
            return dl
    return None



def downloads_dir() -> str:
    """
    Return the downloads directory path with timestamp for
    uniqueness
    """
    ts = datetime.utcnow().strftime('%Y-%m-%d-%H%M%S')
    dir = Path( os.path.dirname(__file__ ) + "/../" ).resolve()
    return f"{dir}/__downloads__/{ts}"


def process_repositories(info:dict, args:Namespace, dir:str):
    """
    """

    g:gh = info['g']
    repos:list = info['repos']
    org:Organization = info['org']
    connection:Github = info['connection']
    total:int = repos.totalCount

    reports:list = []
    missing:list = []
    i:int = 0
    r: Repository.Repository
    for r in repos:
        i = i + 1
        out.group_start(f"[{i}/{total}] Processing repository [{r.name}]")
        dl = download_artifact(r, g, connection, args.organisation_token, dir)
        if dl != None:
            reports.append(dl)
        else:
            missing.append((r.name, r.archived))
        out.group_end()

    out.log(f"Found [{len(reports)}] artifacts to process from [{total}] repositories")



def main():
    """
    Main execution function
    """
    dir = downloads_dir()

    io = handler()
    args = io.parser().parse()

    out.group_start("Github data")
    out.log(f"Getting repositories from Github for [{args.organisation_slug}]")
    info = github_info(args)
    out.log(f"Found [{info['repos'].totalCount}] repositories for [{info['org'].name}]")
    out.group_end()

    process_repositories(info, args, dir)


if __name__ == "__main__":
    main()

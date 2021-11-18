#!/usr/bin/env python
import os
from pathlib import Path
from datetime import datetime
from argparse import Namespace
from pprint import pp
from github.Repository import Repository
from github.MainClass import Github
from github.Organization import Organization
from github.Team import Team

from inputs.handler import handler
from github_extensions import github_extensions,rate_limiter
from out import out


def downloads_dir() -> str:
    """
    Return the downloads directory path with timestamp for
    uniqueness
    """
    ts = datetime.utcnow().strftime('%Y-%m-%d-%H%M%S')
    dir = Path( os.path.dirname(__file__ ) + "/../" ).resolve()
    return f"{dir}/__downloads__/{ts}"


def reports_from_github(args:Namespace, dir:str):
    out.group_start("Github data")

    g:Github = Github(args.organisation_token)
    org:Organization = g.get_organization(args.organisation_slug)
    team:Team = org.get_team_by_slug(args.team_slug)

    out.debug("Setting limiter connection details")
    rate_limiter.CONNECTION = g
    out.debug("Refreshing limiter rates")
    rate_limiter.update()

    repos = team.get_repos()
    total = repos.totalCount
    out.log(f"Found [{total}] repositories for [{org.name}]")
    out.group_end()

    headers = {'Authorization': f"token {args.organisation_token}"}
    i = 0
    reports = []
    missing = []
    r:Repository
    for r in repos:
        i = i + 1
        out.group_start(f"Repository [{i}/{total}] [{r.name}]")

        r = github_extensions.add_repository_extensions(r)
        downloaded = r.download_latest_artifact(dir, headers)
        if downloaded != None:
            reports.append((r.name, downloaded))
        else:
            missing.append((r.name, r.archived))

        out.group_end()

    out.group_start("Summary")
    out.log(f"Found [{len(reports)}/{total}] matching repository artifact reports")
    out.group_end()

    return (reports, missing)


def main():
    """
    Main execution function
    """
    dir = downloads_dir()
    io = handler()
    args = io.parser().parse()

    reports, missing = reports_from_github(args, dir)



if __name__ == "__main__":
    main()

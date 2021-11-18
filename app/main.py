#!/usr/bin/env python
import os
from pathlib import Path
from datetime import datetime
from argparse import Namespace
from pprint import pp
from github import Repository
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



def main():
    """
    Main execution function
    """
    dir = downloads_dir()
    io = handler()
    args = io.parser().parse()

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
    for r in repos:
        i = i + 1
        out.group_start(f"Repository [{i}/{total}] [{r.name}]")

        r = github_extensions.add_repository_extensions(r)
        artifact = r.get_latest_artifact()
        if artifact != None:
            d = artifact.download(f"{dir}/{r.name}/", headers)


        out.group_end()




if __name__ == "__main__":
    main()

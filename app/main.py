#!/usr/bin/env python
import os
import json
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
from templates.table import heading, row
from out import out


def timestamp_directory(dirname:str = "downloads") -> str:
    """
    Return the dirname directory path based on one level above this script
    with timestamp for uniquenes and creates the folder if it doesnt exist
    """
    ts = datetime.utcnow().strftime('%Y-%m-%d-%H%M%S')
    dir = Path( os.path.dirname(__file__ ) + "/../" ).resolve()
    path = Path(f"{dir}/__{dirname}__/{ts}")

    os.makedirs(path, exist_ok=True)
    return path.resolve()



def reports_from_github(args:Namespace, dir:str):
    """
    Fetch the reporting artifacts for each repo the org and team
    has access to
    """
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


def merge_raw_packages(report_files:list, json_file_name:str = "raw.json", json_key:str = "packages") -> list:
    """
    Read all report files in as json, load the package data into
    a list an return all of that data
    """
    packages = []
    out.group_start("Merging packages")
    i = 0
    total = len(report_files)
    for name, dir in report_files:
        i = i +1
        file_path = f"{dir}/{json_file_name}"
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            with open(file_path, 'r') as json_file:
                loaded = json.load(json_file)
                data = loaded.get(json_key, []) if json_key != None else loaded
                out.log(f"[{i}/{total}] Loaded [{len(data)}] packages from [{name}] [{file_path}]")
                packages.extend(data)
        else:
            out.notice(f"[{i}/{total}] Raw report not found / accessible [{file_path}]", "Report missing")


    out.group_end()

    # merge packages that are identical
    packages = [dict(t) for t in {tuple(d.items()) for d in packages}]


    return sorted(packages, key=lambda p: p['name'])


def package_corrections(p:dict) -> dict:
    tags = p.get('tags', "")
    version = p.get('version', None)
    if type(tags) == list:
        p['tags'] = ", ".join(tags)
    if type(version) == dict:
        p['version'] = version.get('version', None)
    return p

def packages_to_html(
    packages:list,
    headers: list = ['name', 'version', 'repository', 'source', 'tags', 'type', 'license']
    ) -> tuple:
    """
    Use packages passed in to create a html table containing a line for each package

    This is different that the older version, but should provided clearer route to finding
    where and which repo what version a packages is
    """

    out.group_start("Generating HTML report")
    head = f"<thead>{heading(headers)}</thead>"

    body = ""
    i = 0
    total = len(packages)
    for p in packages:
        i = i + 1
        p = package_corrections(p)
        out.log(f"[{i}/{total}] Package {p.get('name')}")
        r = row(p, headers)
        body = f"{body}{r}\n"

    table = f"<table>\n{head}\n<tbody>\n{body}\n</tbody>\n</table>"
    dir = timestamp_directory("reports")

    file_path = f"{dir}/report.v1.0.0.html"
    out.debug(f"Writing HTML to [{file_path}]")
    with open(file_path, 'w') as html_file:
        html_file.write(table)
        html_file.close()


    json_path = f"{dir}/report.v1.0.0.json"
    out.debug(f"Writing JSON to [{json_path}]")
    with open(json_path, 'w') as json_file:
        json.dump(packages, json_file)
        json_file.close()

    out.group_end()
    return file_path, json_path


def main():
    """
    Main execution function
    """
    dir = timestamp_directory()
    io = handler()
    args = io.parser().parse()

    reports, missing = reports_from_github(args, dir)
    all_packages = merge_raw_packages(reports)

    html_file, json_file = packages_to_html(all_packages)
    dir = os.path.dirname(html_file)

    out.group_start("Repositories without reports")
    i = 0
    t = len(missing)
    for repo, arch in missing:
        i = i +1
        out.log(f"[{i}/{t}] Repository [{repo}] archived [{arch}]")
    out.group_end()

    out.group_start("Output")
    out.log(f"Generated reports here [{dir}]")
    out.log(f"  HTML report here [{html_file}]")
    out.log(f"  JSON report here [{json_file}]")
    out.set_var("amalgamated_package_scan_report", dir)
    out.group_end()


if __name__ == "__main__":
    main()

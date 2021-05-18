const github = require('@actions/github');

/**
 * Fetch the octokit via the github space
 *
 * @param {string} token
 * @returns
 */
const get = (token) => github.getOctokit(token)

/**
 * Fetch all the repositories that belong to the
 * org and team specified using the octokit object
 *
 * @param {*} octokit
 * @param {string} org
 * @param {string} team
 * @returns
 */
const repos = async (octokit, org, team) => {
    const found = await octokit.paginate(
        octokit.rest.teams.listReposInOrg,
        {org: org, team_slug: team, per_page: 100},
        response => response.data
    )
    return new Promise((resolve) => {resolve(found)})
}

/**
 * Fetch all artifacts for the repository passed in
 *
 * @param {*} octokit
 * @param {*} repo
 * @param {string} org
 * @returns
 */
const artifacts = async (octokit, repo, org) => {
    const found = await octokit.paginate(
        'GET /repos/{owner}/{repo}/actions/artifacts',
        {owner: org, repo: repo.name},
        response => response.data
    )
    return new Promise((resolve) => {resolve(found)})
}

/**
 *
 * @param {*} octokit
 * @param {*} repo
 * @param {string} org
 * @param {string[]} artifactNames
 * @returns
 */
const artifact = async (octokit, repo, org, artifactNames) => {
    const found = await artifacts(octokit, repo, org)
    const first = found.find(i => artifactNames.includes(i.name))

    return new Promise( (resolve, reject) => {
        if(first && first.archive_download_url) resolve([repo, first])
        reject(repo)
    })
}


module.exports = {
    get,
    repos,
    artifacts,
    artifact
}

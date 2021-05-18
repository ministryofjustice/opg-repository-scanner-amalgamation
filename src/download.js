const core = require('@actions/core');

const octokit = require('./octokit')
const zip = require('./zip')

/**
 * Download and extract artifacts that match
 * the name to local file store
 * @param {*} repos
 * @param {*} params
 * @param {*} downloadDirectory
 */
const run = async (octo, repos, params, downloadDirectory) => {
    // async calls to find artifacts and download them
    let promises = []
    for(const repo of repos){
        promises.push( new Promise((resolve) =>
            octokit
            .artifact(octo, repo, params.organisation_slug, params.artifact_names)
            .then( async (data) => {
                const [repo, artifact] = data
                core.info(`[${repo.name}] has an artifact @[${artifact.created_at}].`)
                // now download the file
                await zip.get(repo, artifact, params.token, downloadDirectory)
                resolve()
            })
            .catch((e) => {
                core.debug(e.message || `[${repo.name}] No matching artifacts`)
                resolve()
            })
        ))
    }
    await Promise.allSettled(promises)
}


module.exports = {
    run
}

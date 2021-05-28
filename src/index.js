const core = require('@actions/core');
const artifact = require('@actions/artifact')
const path = require('path')

const inputs = require('./inputs');
const octokit = require('./octokit')
const download = require('./download')
const group = require('./group')
const load = require('./loader')
const f = require('./files')
const as = require('./as')

const version = "v1.0.0"
/**
 *
 */
async function run() {
  // validate the action inputs
  const params = inputs.get()
  inputs.validate(params)
  core.info(`GitHub Action inputs validated.`)

  const downloadBase = path.resolve(params.directory, '__downloads')
  const artifactBase = path.resolve(params.directory, '__artifacts')
  f.mkdir(downloadBase)
  f.mkdir(artifactBase)


  const artifactName = 'amalgamated_package_scan_report'
  const now = Date.now().toString()
  const downloadDir = path.resolve(params.directory, '__downloads', now) + '/'
  const artifactDir = path.resolve(params.directory, '__artifacts', now) + '/'

  // fetch the octokit using the token from the action
  const octo = octokit.get(params.token)
  const repos = await octokit.repos(octo, params.organisation_slug, params.team_slug)
  // do all the downloads
  await download.run(octo, repos, params, downloadDir)
  // get all the report files
  const reportFiles = await f.get(params, downloadDir)
  // merge object to push everything into
  const loaded  = load.fromFiles(reportFiles)
  loaded.packages = group.byName(loaded.packages)
  // save the merged report as json and then markdown
  const jsonFile = f.write(`report.${version}.json`, artifactDir, as.json(loaded) )
  const mkFile = f.write(`report.${version}.md`, artifactDir, as.markdown(loaded) )
  const hFile = f.write(`report.${version}.html`, artifactDir, as.html(loaded) )
  const files = [
    `${artifactDir}report.${version}.json`,
    `${artifactDir}report.${version}.md`,
    `${artifactDir}report.${version}.html`
  ]

  if (jsonFile && mkFile && hFile){
    core.info(`Creating artifact [${artifactName}] for workflow from files: \n - ${files.join('\n - ')}`)
    const client = artifact.create()
    await client.uploadArtifact(artifactName, files, artifactDir, {
      continueOnError: false
    })
  }

}


try {
  run().catch((e) => {
    core.setFailed(e.message);
    console.log(e)
  })
} catch (error) {
  core.setFailed(error.message);
}

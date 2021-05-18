const core = require('@actions/core');

const inputs = require('./inputs');
const octokit = require('./octokit')
const download = require('./download')
const group = require('./group')
const load = require('./loader')
const files = require('./files')
const as = require('./as')

/**
 *
 */
async function run() {
  const now = Date.now()
  const downloadDirectory = `./__downloads-${now}/`
  const artifactDir = `./__artifact-${now}/`
  // validate the action inputs
  const params = inputs.get()
  inputs.validate(params)
  core.info(`GitHub Action inputs validated.`)

  // fetch the octokit using the token from the action
  const octo = octokit.get(params.token)
  const repos = await octokit.repos(octo, params.organisation_slug, params.team_slug)
  // do all the downloads
  await download.get(octo, repos, params, downloadDirectory)
  // get all the report files
  const reportFiles = await files.get(params, downloadDirectory)

  // merge object to push everything into
  const loaded  = load.fromFiles(reportFiles)
  loaded.packages = group.byName(loaded.packages)

  // save the merged report as json and then markdown
  files.write("report.v1.json", artifactDir, as.json(loaded) )
  files.write("report.v1.md", artifactDir, as.markdown(loaded) )

}



try {
  run()
} catch (error) {
  core.setFailed(error.message);
}

const core = require('@actions/core');
const artifact = require('@actions/artifact')

const inputs = require('./inputs');
const octokit = require('./octokit')
const download = require('./download')
const group = require('./group')
const load = require('./loader')
const files = require('./files')
const as = require('./as')

const version = "v1.0.0"
/**
 *
 */
async function run() {
  const artifactName = 'merged-report'
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
  await download.run(octo, repos, params, downloadDirectory)
  // get all the report files
  const reportFiles = await files.get(params, downloadDirectory)
  // merge object to push everything into
  const loaded  = load.fromFiles(reportFiles)
  loaded.packages = group.byName(loaded.packages)
  // save the merged report as json and then markdown
  const jsonFile = files.write(`report.${version}.json`, artifactDir, as.json(loaded) )
  const mkFile = files.write(`report.${version}.md`, artifactDir, as.markdown(loaded) )
  const files = [ `${artifactDir}report.${version}.json`, `${artifactDir}report.${version}.md` ]

  if (jsonFile && mkFile){
    core.info(`Creating artifact for workflow from files: \n - ${files.join('\n - ')}`)
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

const glob = require('@actions/glob');

/**
 * Fetch all files that match the report_name files
 * within the downloadDirectory and return promise of
 * string array
 * @param {object} params
 * @param {string} downloadDirectory
 * @returns
 */
const get = async (params, downloadDirectory) => {
  // now find all the files that match the report names we're looking for
  // and we'll then merges those together
  let reportFiles = []
  for(const file of params.report_names) {
    const pattern = downloadDirectory + '**/' + file
    const glober = await glob.create(pattern, {followSymbolicLinks: false})
    reportFiles.push( ...await glober.glob() )
  }

  return new Promise( (resolve) => resolve(reportFiles) )
}

module.exports = {
    get
}

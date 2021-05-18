const glob = require('@actions/glob');
const fs = require('fs')
const path = require('path')

const trim = (dir) => dir.replace(/\/$/, "") + '/'
const mkdir = (dir) => { if(! fs.existsSync(dir)) fs.mkdirSync(dir) }


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

/**
 * Write content to file and return if the file exists
 * @param {string} file
 * @param {string} directory
 * @param {string} content
 * @returns
 */
const write = (file, directory, content) => {
  const dir = trim(directory)
  mkdir(dir)

  const filepath = path.resolve(dir, file)
  fs.writeFileSync(filepath, content)
  return fs.existsSync(filepath)

}


module.exports = {
  trim,
  mkdir,
  get,
  write
}

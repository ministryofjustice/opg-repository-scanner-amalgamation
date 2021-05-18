const axios = require('axios')
const fs = require('fs')
const path = require('path')
const unzipper = require('unzipper')
const core = require('@actions/core');

const files = require('./files')

/**
 * Downloads the {source} file to {file} in {dir}
 *
 * @param {string} source
 * @param {string} dir
 * @param {string} file
 * @returns
 */
const download = async (source, dir, file) => {
    dir = files.trim(dir)
    files.mkdir(dir)

    const destination = path.resolve(dir, file)
    await axios.get(source, {responseType: 'arraybuffer'}).then((response) => {
        fs.writeFileSync(destination, response.data)
    })

    return new Promise((resolve) => resolve(fs.existsSync(destination)) )
}

/**
 * Extracts {source} zip file to the {target} directory under
 *  {dir}
 * @param {string} source
 * @param {string} dir
 * @param {string} target
 */
const extract = async (source, dir, target) => {
    dir = files.trim(dir)
    target = files.trim(target)
    const destination = path.resolve(dir, target)
    const stream  = fs .createReadStream(source)

    stream.pipe( unzipper.Extract( {path: destination} ) )

    await new Promise((resolve) => {
        stream.on('close', () => resolve())
    })
}

/**
 *
 * @param {*} repo
 * @param {*} artifact
 * @param {*} token
 * @param {*} dir
 * @returns
 */
const get = async (repo, artifact, token, dir) => {
    dir = files.trim(dir)
    const url = artifact.archive_download_url
    const tokenUrl = url.replace('api.', `${token}@api.`)

    core.info(`Downloading ${url}`)

    await download( tokenUrl, dir, `${repo.name}.zip`)

    core.info(`Extracting ${dir}${repo.name}.zip`)
    await extract(`${dir}${repo.name}.zip`, dir, repo.name)

    return new Promise((resolve) => resolve() )
}

module.exports = {download, extract, get}

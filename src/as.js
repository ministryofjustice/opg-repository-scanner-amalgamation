
/**
 *
 * @param {object} object
 * @returns
 */
const json = (object) => {
    return JSON.stringify(object)
}


/**
 * Generate markdown string from list of packages
 * @param {string[]} packages
 * @returns
 */
const packagesMarkdown = (packages) => {
    let markdown = "| Package | Repositories | Version | Occurances | Tags | Licenses |\n| -- | -- | -- | -- | -- | -- |\n"

    for(const row of packages){
        markdown += `| ${row.name} `
        const cols = [ row.repository, row.version, row.source, row.tags, row.license]
        for(const col of cols) markdown += `| ${col.join('<br>').replace(/\|/g, "\\|")} `
        markdown += "|\n"
    }
    return markdown
}
/**
 *
 * @param {*} object
 */
const markdown = (object) => {
    return packagesMarkdown(object.packages)
}


module.exports = {
    json,
    markdown
}

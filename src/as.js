var slugify = require('slugify')

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

const packagesHtml = (packages) => {
    let html = `
    <table class='filter'>
        <thead>
            <tr>
                <th>Package</th>
                <th>Repositories</th>
                <th>Versions</th>
                <th>Occurances</th>
                <th>Tags</th>
                <th>Licenses</th>
            </tr>
        </thead>
        <tbody>\n`
    packages = packages.sort((a, b) => {
        if (a.name > b.name) return 1
        else if (a.name < b.name ) return -1
        return 0
     })
    for(const row of packages){
        const rowid = slugify(row.name)
        html += `<tr><th id='package-${rowid}'>${row.name}</th>`
        const cols = [ row.repository, row.version, row.source, row.tags, row.license]
        for(const col of cols){
            if (col.length > 0) html += `<td data-len="${col.length}"><ul><li>${col.join('</li><li>')}</li></ul></td>`
            else html += `<td data-len="${col.length}"></td>`
        }
        html += "</tr>\n"
    }
    return `${html}</tbody></table>`
}
/**
 *
 * @param {*} object
 */
const markdown = (object) => {
    return packagesMarkdown(object.packages)
}


const html = (object) => {
    return packagesHtml(object.packages)
}

module.exports = {
    json,
    markdown,
    html
}

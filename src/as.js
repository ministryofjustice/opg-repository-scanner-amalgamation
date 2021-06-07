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
                <th class='col col-package'>Package</th>
                <th class='col col-repositories'>Repositories</th>
                <th class='col col-versions'>Versions</th>
                <th class='col col-occurances'>Occurances</th>
                <th class='col col-tags'>Tags</th>
                <th class='col col-licenses'>Licenses</th>
            </tr>
        </thead>
        <tbody>\n`
    packages = packages.sort((a, b) => {
        if (a.name > b.name) return 1
        else if (a.name < b.name ) return -1
        return 0
     })
    for(const row of packages){
        const rowid = slugify(row.name).replace("@", "")
        html += `<tr><th id='package-${rowid}' class='col col-package'>${row.name}</th>`
        const cols = { repositories:row.repository, versions: row.version, occurances: row.source, tags: row.tags, licenses: row.license }
        for(const [key, col] of Object.entries(cols) ){
            if (col.length > 0) html += `<td data-len="${col.length}" class="col col-${key}"><ul><li>${col.join('</li><li>')}</li></ul></td>`
            else html += `<td data-len="${col.length}" class="col col-${key}"></td>`
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

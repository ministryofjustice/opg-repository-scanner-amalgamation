const fs = require('fs')


/**
 * Create an object based on the entries from all file
 * content
 * @param {string[]} reportFiles
 * @returns
 */
 const fromFiles = (reportFiles) => {
    let object = {}

    for(const f of reportFiles) {
        const parsed = JSON.parse(fs.readFileSync(f, 'utf8'))
        for (const key of Object.keys(parsed) ) {
            if(typeof object[key] === 'undefined') object[key] = []
            object[key].push(...parsed[key])
        }
    }
    return object
}


module.exports = {
    fromFiles
}

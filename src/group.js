/**
 *
 * @param {object[]} packages
 */
const byName = (packages) => {
    let reduced = []
    const uniqueNames = [ ...new Set( packages.map(pkg => pkg.name) ) ]
    // loop over all names
    for (const name of uniqueNames) {
        let matched = packages.filter(i => (i.name === name ))
        let pkg = {name: matched[0].name}
        // these cols are all map able and run filter to remove empties
        let cols = ['repository', 'version', 'type', 'license', 'source']
        for(const c of cols) pkg[c] = [ ...new Set(matched.map(p => p[c] ))].filter(i => i)
        // tags are a flat string with , split.. so join them together and then
        // reform an array to remove duplicates
        pkg.tags = [
            ...new Set(
                matched
                    .reduce((str, i) => {str += `${i.tags},`; return str}, "" )
                    .split(',')
                    .map(i => i.trim())
            )
        ].filter(i => i)

        reduced.push(pkg)
    }
    return reduced
}

module.exports = {
    byName
}

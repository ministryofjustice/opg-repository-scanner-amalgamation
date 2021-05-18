const { expect } = require('@jest/globals')
const group = require('../src/group')
const load = require('../src/loader')

test(`Test grouping by package name`, async () => {
    let pkgs = [
        {
            "repository": "test-repo1",
            "name": "requests-aws4auth",
            "version": "1.0.1",
            "type": "manifest",
            "source": "./requirements.txt",
            "license": "",
            "tags": "manifest, python, pip"
        },
        {
            "repository": "test-repo2",
            "name": "requests-aws4auth",
            "version": "1.1.0",
            "type": "manifest",
            "source": "./requirements.txt",
            "license": "",
            "tags": "manifest, python, pip"
        },
        {
            "repository": "test-repo1",
            "name": "something-else",
            "version": "1.0.1",
            "type": "manifest",
            "source": "./requirements.txt",
            "license": "",
            "tags": "manifest, python, pip"
        }
    ]
    pkgs = group.byName(pkgs)
    expect(pkgs.length).toEqual(2)
    const aws = pkgs.find(i => i.name === "requests-aws4auth")
    // should have 2 entries
    expect(aws.repository.length).toEqual(2)

})


test(`Test grouping by package name using large samples`, async () => {

    const files = [
        // 4818 items
        './tests/samples/opg-lpa.json',
        // 2952 items
        './tests/samples/opg-digideps.json'
    ]
    const loaded = load.fromFiles(files)
    const grouped = group.byName(loaded.packages)
    // this exists in both (added to digideps)
    const pkgs = grouped.find(i => i.name === 'requests-aws4auth' )
    expect(pkgs.repository.length).toEqual(2)

})

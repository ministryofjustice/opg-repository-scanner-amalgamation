
const { expect } = require('@jest/globals')
const load = require('../src/loader')


test(`Test loading object from files`, async () => {
    const files = [
        // 4818 items
        './tests/samples/opg-lpa.json',
        // 2952 items
        './tests/samples/opg-digideps.json'
    ]
    const object = load.fromFiles(files)
    expect(object.packages).toBeTruthy()
    expect(object.packages.length).toEqual(7770)
})

const { expect } = require('@jest/globals')
const files = require('../src/files')

test(`Test finding files`, async () => {
    const params = { report_names: ['*.json'] }
    const dir = 'tests/samples/'
    const found = await files.get(params, dir)

    expect(found.length).toEqual(2)

})

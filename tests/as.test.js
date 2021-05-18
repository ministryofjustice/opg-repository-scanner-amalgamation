const { expect } = require('@jest/globals')
const as = require('../src/as')

test(`Test as json stringify`, async () => {
    const original = "{\"tester\":\"testv1\",\"packages\":[\"test\"]}"
    const parse = JSON.parse(original)
    const str = as.json(parse)
    expect(str).toEqual(original)
})


test(`Test as markdown conversion`, async () => {
    const match =
        '| Package | Repositories | Version | Occurances | Tags | Licenses |\n' +
        '| -- | -- | -- | -- | -- | -- |\n' +
        '| test | one | v1.0 | test.js | test<br>php | MIT |\n'

    const packages = {
        packages:[
            {
                name: 'test',
                repository: ['one'],
                version: ['v1.0'],
                source: ['test.js'],
                tags: ['test', 'php'],
                license: ['MIT']
            }
        ]
    }
    const mk = as.markdown(packages)
    expect(mk).toEqual(match)
})

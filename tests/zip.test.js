const zip = require('../src/zip')
const fs = require('fs')
const { expect } = require('@jest/globals')


test(`Test zip download and extract using govuk-frontend release zip`, async () => {
    const dir = './tests/__ziptest/'
    // remove the directory
    fs.rmdirSync(dir, { recursive: true })


    const zipfile = 'tmp.zip'
    const url = 'https://github.com/alphagov/govuk-frontend/releases/download/v3.12.0/release-v3.12.0.zip'
    const dl = await zip.download(url, dir, zipfile)

    expect(dl).toBeTruthy()
    const zipexists = fs.existsSync(dir + zipfile)
    expect(zipexists).toBeTruthy()

    // size check
    const stats = fs.statSync(dir + zipfile)
    const size = stats.size / (1024);
    expect(size).toBeGreaterThanOrEqual(200)

    // extract and test the version file exists
    await zip.extract(dir + zipfile, dir, 'tester/')

    const filepath = dir + 'tester/VERSION.txt'
    const exists = fs.existsSync(filepath)
    expect(exists).toBeTruthy()

    // clean up, but with a pause
    setTimeout(() => fs.rmdirSync(dir, { recursive: true }), 1000)

})

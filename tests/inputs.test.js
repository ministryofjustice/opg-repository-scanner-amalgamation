const { expect } = require('@jest/globals')
const inputParams = require('../src/inputs')

test(`Test inputParameters is all false without process env vars`, async () => {
    const params = inputParams.get()
    const entities = Object.entries(params)
    const falsey = entities.filter(i => i.pop() === false)

    expect(falsey.length).toEqual(entities.length)

})


test(`Test inputParameters is all false except for team slug`, async () => {
    // set a team slug for this test
    process.env.INPUT_TEAM_SLUG = 'test'
    const params = inputParams.get()
    const entities = Object.entries(params)
    const falsey = entities.filter(i => i.pop() === false)

    expect(falsey.length).toEqual(entities.length - 1)

})


test(`Test validInputParameters throws an exception without env vars`, async () => {
    const params = inputParams.get()
    expect.assertions(1)
    try{
        inputParams.validate(params)
    } catch (e) {
        expect(e).toBeInstanceOf(Error)
    }
})


test(`Test validInputParameters validates with env vars set`, async () => {
    // set this processes env vars
    process.env.INPUT_ORGANISATION_TOKEN = 'test'
    process.env.INPUT_TEAM_SLUG = 'test'
    process.env.INPUT_ORGANISATION_SLUG = 'test'
    process.env.INPUT_ARTIFACT_NAMES = 'test1,test2'
    process.env.INPUT_REPORT_NAMES = 'test'
    process.env.INPUT_DIRECTORY = './'

    const params = inputParams.get()
    const valid = inputParams.validate(params)

    expect(valid).toBeTruthy()

    expect(params.artifact_names.length).toEqual(2)
    expect(params.report_names.length).toEqual(1)

})

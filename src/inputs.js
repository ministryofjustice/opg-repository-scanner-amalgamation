const core = require('@actions/core');

/**
 * Custom error
 */
class InputError extends Error {
    constructor(...args) {
        super(...args)
        Error.captureStackTrace(this, InputError)
    }
}

/**
 * If this is an array, then return the string split
 * by the ,
 * Otherwise, return the value or false directly
 *
 * @param {string} name
 * @param {boolean} isArray
 * @returns {string|boolean}
 */
const input = (name, isArray) => {
    const val = core.getInput(name)
    if (isArray &&  val.length > 0) return val.split(',')
    else if (!isArray) return val || false
    return false
}


/**
 * Generate an object of input parameters
 * @returns {object}
 */
const get = () => {
    return {
        token: input('organisation_token', false),
        organisation_slug: input('organisation_slug', false),
        team_slug: input('team_slug', false),
        artifact_names: input('artifact_names', true),
        report_names: input('report_names', true),
        directory: input('directory', false)
    }
}

/**
 * Validate that {params} contains all the required
 * input, otherwise throw an error detailing whats missing
 * @param {object} params
 */
const validate = (params) => {
    const invalidEntries = Object
                                .entries( params )
                                .filter(row => row.pop() === false )

    if (invalidEntries.length > 0) {
        throw new InputError(`the following input params were missing:\n - ${invalidEntries.join('\n - ')}`)
    }
    return true
}

module.exports = {
    get,
    validate
}

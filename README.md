# OPG Repository Scanner Amalgamation

This action is intended to fetch all repository scan results and merge them into a single report which can then be shown centrally.

## Inputs

### `organisation_slug`

**Default: `opg`**

The slug of the github organisation we are fetching reports from.

### `organisation_token`

Token used to access the github organisation and its teams.

### `team_slug` **\***

The GitHub team within the organisation whose repositories we are going to check.


## Output

This action generates an artifact containing the merged reports in a html and json file.

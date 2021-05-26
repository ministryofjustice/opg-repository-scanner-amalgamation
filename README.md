# OPG Repository Scanner Amalgamation

This action is intended to fetch all repository scan results and merge them into a single report which can then be shown centrally.

## Inputs

Currently, GitHub actions dont allow for complex / nested variable structures, so where required inputs are coverted using `JSON.parse` - these are marked with a **\***

### `organisation_slug`

**Default: `opg`**

The slug of the github organisation we are fetching reports from.

### `organisation_token`

Token used to access the github organisation and its teams.

### `team_slug` **\***

The GitHub team within the organisation whose repositories we are going to check.

### `artifact_names`

**Default: `'repository-scan-result'`**

List of artifacts that this tool wants to merge together. Looks for this name against the repositories known workflow artifacts.

### `report_name`

**Default: `'raw.json'`**

List of reports out of the artifacts we want to use for this tool. These reports are merged into the single report.

### `directory`

**Default: `${{ github.workspace }}`**

Directory to write files to.


## Output

This action generates an artifact containing the merged reports in a markdown and json file.

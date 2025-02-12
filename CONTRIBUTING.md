## Contributing Guidelines
This repository stores GitHub actions via reusable workflows.
https://resources.github.com/learn/pathways/automation/intermediate/create-reusable-workflows-in-github-actions/

When implementing the workflows in repositories, we chose to reference this repository's `main` branch. This trade-off allows us to update scanning configurations and make changes without needing to then update each dependent repository.

**NOTE**: This trade-off *also* means there is a risk for introducing changes that are not properly tested.

## Test All Changes
- Create and push any changes to a feature branch prior to opening a PR (e.g `update-setup-node-version`).
- Choose 1-2 dependent application repositories that reference all workflows being changed.
- Create a branch on each of the chosen repositories (e.g. `test-security-workflows-node-version`).
- Within each changed workflow, update the branch reference to the feature branch within the application's workflow files.
```
# repo: chargehound/<dependent-application-repo>
# path: .github/workflows/security.code-scanning.yml

jobs:
  codeql-javascript:
    uses: chargehound/security-workflows-public/.github/workflows/codeql-javascript.yml@update-setup-node-version
```
- Push these changes to the application's branch (e.g. `test-security-workflows-node-version`)
- Navigate to the application repository's Actions tab
- Choose the relevant Action (CodeQL / Dependency Review)
- Select the test branch (e.g. `test-security-workflows-node-version`) under the workflow_dispatch `Run workflow` options.
- Run the scan and check for successful scan.
- Navigate to the appliation repository's Security tab and choose the relevant scanner.
- Filter the results to the test branch and ensure results match the default branch.


## Pull Requests
- Please write a description outlining the changes made including any relevant Jira tickets.
- Include links to the successful test results on the example dependent applications.
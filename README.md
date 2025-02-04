# Get Snyk Organisation Details

Lists Snyk Organisations in a Group and their Integrations.

## Features

`get_orgs.py` - gathers Organisation information for entire Snyk Group. 

Uses [Snyk's REST API](https://apidocs.snyk.io/?version=2024-10-15#get-/groups/-group_id-/orgs) for getting the Orgs and [Snyk's V1 API](https://snyk.docs.apiary.io/#reference/integrations/integrations/list) for integration information.

## Configuration

### Adjust local script settings

Install dependencies
```sh
pip install -r requirements.txt
```

Update variables in `get_orgs.py`. Get the latest API Version from [Snyk's REST API](https://apidocs.snyk.io/)
```py
API_VERSION = "2024-08-15"
RATE_LIMIT_DELAY = 0.2 (in seconds)
```

Update the value of `workflow_repo_name` in `import_projects.py` to the name of the repository owning the import workflow.
```py
# Name of the repo owning the import workflow
workflow_repo_name="snyk-pavski/snyk-auto-imports"
```

### Configure Github Actions Workflow

1. Set necessarry secrets up:

    ```
    secrets.GH_TOKEN    # See link below
    secrets.SNYK_PAT    # Use a Personal PAT or a Service Account PAT
    secrets.SNYK_API    # https://api.snyk.io/v1 / https://api.eu.snyk.io/v1

    secrets.GIT_EMAIL
    secrets.GIT_USERNAME
    ```
    [GH Token Requirenments](https://docs.snyk.io/scm-ide-and-ci-cd-integrations/snyk-scm-integrations/github-enterprise#generate-a-personal-access-token-from-your-github-settings)


2.  Configure new worklow per **GHA_main.yaml** file.



## Usage

### Gather Org and Integration information.

```sh
python3 get_orgs.py --group YOUR_GROUP_ID --token YOUR_API_TOKEN
```

Script will output each Snyk Organisation in the Group provided together with the ID of Github Integration. 

```sh
Snyk Org Name: ExampleOrg1 - Org ID: xxx - GH Integration ID: xxx
Snyk Org Name: ExampleOrg2 - Org ID: xxx - GH Integration ID: xxx
Snyk Org Name: ExampleOrg3 - Org ID: xxx - GH Integration ID: xxx
```

### Raise a new Project Import Pull Request.

Run the script and follow the prompts:

```sh
python3 import_projects.py
```

```sh
Enter the GitHub Org (owner) name: ***
Enter the repository name you want to import: ***
Enter the branch name you want to import: ***
Enter the ID of your Snyk Org: ***
Enter the ID of your Snyk Integration: ***
```

This should output the new target added to the file and raise a new Pull Request with new Target to be imported.

```sh
Updated import-projects.json with the new target:
{
    "orgId": "***",
    "integrationId": "***",
    "target": {
        "name": "***",
        "owner": "***",
        "branch": "***"
    }
}
```

Merging the PR should trigger the Import Workflow

import json
import os
import subprocess

# Name of the repo owning the import workflow
workflow_repo_name="snyk-pavski/snyk-auto-imports"

# File path for import-projects.json
json_file = 'import-projects.json'

# Read the existing JSON and append the new target
def update_json_file(orgId, integrationId, owner, repo_choice, branch_name):
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
    else:
        # Initialize a new structure if the file doesn't exist
        data = {"targets": []}  

    # New target to be added
    new_target = {
        "orgId": orgId,
        "integrationId": integrationId,
        "target": {
            "name": repo_choice,
            "owner": owner,
            "branch": branch_name
        }
    }

    data["targets"].append(new_target)

    # Write the updated data back to the JSON file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

    print(f'Updated {json_file} with the new target:')
    print(json.dumps(new_target, indent=4))

# Function to create a PR in the GitHub repository
def create_pr(branch_name):
    # Get the current branch before creating a new one
    current_branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True).stdout.strip()

    # Pull the latest import-targets.json
    # subprocess.run(["git", "fetch", "origin", current_branch], check=True) 
    
    subprocess.run(["git", "checkout", "-b", branch_name])
    subprocess.run(["git", "add", json_file])
    commit_message = f"Add new import target for {branch_name}"
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push", "origin", branch_name])
    subprocess.run(["gh", "pr", "create", "--title", commit_message, "--body", "Adding new import target", "--repo", workflow_repo_name])
    subprocess.run(["git", "checkout", current_branch], check=True)

    print(f"Switched back to branch: {current_branch}")


# Main function to ask for inputs and update the JSON
def main():
    org_choice = input("Enter the GitHub Org (owner) name: ").strip()
    repo_choice = input("Enter the repository name you want to import: ").strip()
    branch_choice = input("Enter the branch name you want to import: ").strip()
    orgId = input("Enter the ID of your Snyk Org: ").strip()
    integrationId = input("Enter the ID of your Snyk Integration: ").strip()

    current_branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True).stdout.strip()
    subprocess.run(["git", "pull"], check=True)
    print(f"Pulled the latest changes in: {current_branch}")

    # Update the JSON file with the provided details
    update_json_file(orgId, integrationId, org_choice, repo_choice, branch_choice)

    # Create a PR with the changes
    pr_branch_name = input("Enter the name of the new branch for the PR: ").strip()
    create_pr(pr_branch_name)

if __name__ == "__main__":
    main()

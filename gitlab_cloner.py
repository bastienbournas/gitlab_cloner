import requests
import os
import subprocess
import argparse

# Function to fetch all repositories using GitLab API
def get_all_repos(gitlab_url, token):
    repos = []
    page = 1
    while True:
        print(f"Fetching page {page}...")

        response = requests.get(
            f"{gitlab_url}/api/v4/projects",
            headers={"PRIVATE-TOKEN": token},
            params={"per_page": 100, "page": page}
        )

        if response.status_code != 200:
            print(f"Error fetching projects: HTTP {response.status_code} - {response.text}")
            break

        data = response.json()
        print(f"Received {len(data)} projects on page {page}")

        if not data:
            print("No more projects found.")
            break  # Stop if there are no more projects

        repos.extend(data)
        page += 1

    print(f"Total repositories found: {len(repos)}")
    return repos

# Function to clone each repository
def clone_repos(repos, gitlab_url, token, output_dir):
    for repo in repos:
        repo_name = repo["path_with_namespace"]
        http_url = repo.get("http_url_to_repo")

        if not http_url:
            print(f"Skipping {repo_name} - No HTTP clone URL found.")
            continue

        # Append the token to the HTTP URL for cloning
        clone_url = http_url.replace("https://", f"https://oauth2:{token}@")

        # Local path to clone into
        repo_dir = os.path.join(output_dir, repo_name.replace("/", "_"))

        # Skip if already cloned
        if os.path.exists(repo_dir):
            print(f"Skipping {repo_name} - Already cloned.")
            continue

        print(f"Cloning {repo_name} from {clone_url}...")

        try:
            subprocess.run(["git", "clone", clone_url, repo_dir], check=True)
            print(f"Successfully cloned {repo_name}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone {repo_name}: {e}")

# Main script execution
if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Clone all repositories from a GitLab instance.")
    parser.add_argument("--gitlab-url", required=True, help="URL of the GitLab instance")
    parser.add_argument("--token", required=True, help="GitLab admin token with appropriate permissions")
    parser.add_argument("--output-dir", default="gitlab_repos", help="Directory where repositories will be cloned")
    args = parser.parse_args()

    # Ensure the output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Fetch the list of repositories
    repos = get_all_repos(args.gitlab_url, args.token)

    # Clone the repositories if any are found
    if repos:
        clone_repos(repos, args.gitlab_url, args.token, args.output_dir)
    else:
        print("No repositories found or access token permissions may be insufficient.")

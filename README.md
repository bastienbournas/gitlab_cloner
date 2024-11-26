# Gitlab Cloner
This script relies on the gitlab API to clone every repository from a gitlab instance. 
Run it with gitlab admin token to be able to have 100% of the repos.
# Usage
Pass the url and token to the script (output-dir is optional and defaults to "gitlab_repos").

    python3 gitlab_cloner.py --gitlab-url https://your.gitlab.url.com --token XXX --output-dir gitlab_repos

As this can take a lot of time for big gitlab instance, you can run it as a background process and keep it alive even if ssh session is closed with nohup:

    nohup python3 -u gitlab_cloner.py --gitlab-url https://your.gitlab.url.com --token XXX --output-dir gitlab_repos >> output.log 2>&1 &

# github-scripts
GitHub Scripts

enable_req_status_check.py helps to enable **"Require status checks to pass before merging"** of Branches. <br />
This tool requires GitHub **Personal Access Token** , export your Token to environment with key **GITHUB_API_TOKEN**
> export GITHUB_API_TOKEN='832........345'

It works in two ways:

1. Pass the *.txt* file argument along with **-f**  <br />
Format of *.txt* file should be **repo_name**,**branch_name**<br />
if **branch_name** is not provided **master** will be taken as default. <br />
>example: python3 enable_req_status_check.py *-f* REPO_BRANCH_LIST.txt

2. Pass Repo name and branch name along with **-r and -f**
>example: python3 enable_req_status_check.py *-r* qw-bot *-b* master <br />
**OR** <br />
> python3 enable_req_status_check.py *-r* qw-bot

If *-b* is not provided, **master** branch will be considered as default. 


import os
import logging
import requests
import json
import argparse


def shortenMiddle(s, n):
    sLen = len(s)
    if sLen > n:
        halfN = int(n / 2)
        return s[:halfN] + '...' + s[-halfN:]
    return s


logger = logging.getLogger('enable_req_status_check')
logger.setLevel(logging.DEBUG)
logger.handlers = []

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
logger.addHandler(sh)

ghRootEndpoint = 'https://api.github.com'
requestStatusEnableURL = "/repos/RealImage/{repo}/branches/{branch}/protection"
getStatusCheckURL = requestStatusEnableURL+"/required_status_checks"

ghAPIToken = os.environ['GITHUB_API_TOKEN']
logger.info("GITHUB_API_TOKEN='{}'".format(shortenMiddle(ghAPIToken, 6)))
headers = {'Authorization': 'token ' + ghAPIToken}

payload = json.dumps(
    {
        "required_status_checks":
            {
                "strict": True,
                "contexts": []
            },
        "enforce_admins": None,
        "required_pull_request_reviews": None,
        "restrictions": None
    })


# repoBranchTxt = open("REPO_BRANCH_LIST.txt", "r").read()

def main(inputtextfile):
    global repoBranchPair
    # repoBranchTxt = open("{}.txt".format(inputtextfile), "r").read()
    repoBranchTxt = open(inputtextfile, "r").read()
    reposAndBranchesList = repoBranchTxt.split('\n')

    for repoBranchPair in reposAndBranchesList:
        repoBranchPair = repoBranchPair.split(',')
    if len(repoBranchPair) == 2:
        branch = repoBranchPair[1]
    else:
        branch = 'master'

    enableReqStatCheck(repoBranchPair[0], branch)


def enableReqStatCheck(repo, branch):
    getStatusCheckURLformated = getStatusCheckURL.format(repo=repo,branch=branch)

    ghApiGetresponse = requests.get(ghRootEndpoint + getStatusCheckURLformated,
                                    headers=headers
                                    ).json()

    if not (ghApiGetresponse.get('strict')):

        requestStatusEnableURLformated = requestStatusEnableURL.format(repo=repo,
                                                                       branch=branch)
        logger.info("--Enabling Require status checks to pass before merging--")

        ghApiPutResponse = requests.put(ghRootEndpoint + requestStatusEnableURLformated,
                                        payload,
                                        headers=headers
                                        ).json()
        logger.info(ghApiPutResponse)

    else:
        logger.info("ALREADY ENABLED")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='Enable Request Status Check',
                                     usage='''
                                     provide the text file of Repos and Branches as an argument with -f 
                                     OR
                                     provide repo and branch names as arguments with -r and -b 
                                     ''',
                                     description='''
                                     ------------------------------------------------------------------------------
                                     Description: 
                                     
                                     This tool will enables the Request status checks of braches 
                                     mention in text file OR from stdin
                                     ------------------------------------------------------------------------------   
                                     ''',
                                     add_help=True
                                     )
    parser.add_argument("--file", "-f", type=str, help="Enter the name of TXT file as an argument", metavar="Text file Name: ")
    parser.add_argument("--repo", "-r", type=str, help="Enter the Rpeo name as an argument", metavar="Repository Name")
    parser.add_argument("--branch", "-b", type=str, help="Enter the branch name as an argument", metavar="Branch Name")
    arg = parser.parse_args()

    if arg.file is not None:
        main(arg.file)
    else:
        if arg.branch is None:
            branch = "master"
        else:
            branch = arg.branch

        enableReqStatCheck(arg.repo, branch)


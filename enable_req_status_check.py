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


logger = logging.getLogger('req_stat_chk')
logger.setLevel(logging.DEBUG)
logger.handlers = []

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
logger.addHandler(sh)

ghRootEndpoint = 'https://api.github.com'
getStatusCheckURL = "/repos/RealImage/{repo}/branches/{branch}/protection/required_status_checks"
requestStatusEnableURL = "/repos/RealImage/{repo}/branches/{branch}/protection"



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
    repoBranchTxt = open("{}.txt".format(inputtextfile), "r").read()
    reposAndBranchesList = repoBranchTxt.split('\n')

    for repoBranchPair in reposAndBranchesList:
        repoBranchPair = repoBranchPair.split(',')
    if len(repoBranchPair) == 2:
        branch = repoBranchPair[1]
    else:
        branch = 'master'

    getStatusCheckURLformated = getStatusCheckURL.format(repo=repoBranchPair[0], branch=branch)

    ghApiGetresponse = requests.get(ghRootEndpoint + getStatusCheckURLformated,
                                    headers=headers
                                    ).json()
    # logger.info(ghApiGetresponse)
    if not (ghApiGetresponse.get('strict')):

        requestStatusEnableURLformated = requestStatusEnableURL.format(repo=repoBranchPair[0],
                                                                       branch=branch)
        logger.info("--Enabling Require status checks to pass before merging--")

        ghApiPutResponse = requests.put(ghRootEndpoint + requestStatusEnableURLformated,
                                        payload,
                                        headers=headers
                                        ).json()
        logger.info(ghApiPutResponse)

    else:
        logger.info("ALREADY ENABLED")


# def takeRepoBranchPari(repo,branch):



if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='Enable Request Status Check',
                                     usage='''
                                     provide the text file of Repos and Branches as an argument
                                     ''',
                                     description='''
                                     ------------------------------------------------------------------------------
                                     Description: 
                                     
                                     This tool will enables the Request status checks of braches 
                                     mention in text file.
                                     ------------------------------------------------------------------------------   
                                     ''',
                                     add_help=True
                                     )
    parser.add_argument("--file", "-f", type=str, help="Enter the name of TXT file", metavar="Text file Name: ")
    parser.add_argument("--repo", "-r", type=str, help="Enter the Rpeo name", metavar="Repository Name")
    parser.add_argument("--branch", "-b", type=str, help="Enter the branch name", metavar="Branch Name")
    arg = parser.parse_args()

    if arg.file is not None:
        main(arg.file)
    else:
        if arg.branch is None:
            branch = "master"
        else:
            branch = arg.branch

        ghApiPutResponse = requests.put(
            ghRootEndpoint + "/repos/RealImage/{repo}/branches/{branch}/protection".format(repo=arg.repo,
                                                                                           branch=branch),
            payload,
            headers=headers).json()

        logger.info(ghApiPutResponse)

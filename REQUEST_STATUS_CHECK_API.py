import os
import requests
import logging
from io import StringIO
import urllib.request 
import requests
import json

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

ghAPIToken = os.environ['GITHUB_API_TOKEN']
logger.info("GITHUB_API_TOKEN='{}'".format(shortenMiddle(ghAPIToken, 6)))

REPO_AND_BRANCH_txt = open("REPO_BRANCH_LIST_BH.txt","r").read()

reposAndBranches = REPO_AND_BRANCH_txt.split('\n')

for repoBranchPair in reposAndBranches:
    repoBranchPair= repoBranchPair.split(',')
    if len(repoBranchPair) == 2:
        branch = repoBranchPair[1]
    else:
        branch = 'master'
        
    getStatusCheckURL = "/repos/backdoorHall/{repo}/branches/{branch}/protection/required_status_checks".format(repo = repoBranchPair[0],branch = branch)
    
    ghAPIresponse = requests.get(ghRootEndpoint+getStatusCheckURL,\
                          headers={'Authorization':'token ' + ghAPIToken}).json()
    #logger.info(ghAPIresponse)
    if not (ghAPIresponse.get('strict')):
        protected_URL = "/repos/backdoorHall/{repo}/branches/{branch}/protection".format(repo = repoBranchPair[0],branch= branch )
        print("=====working on PATCH====")
        payload = json.dumps({"required_status_checks": {
    "strict": True,
    "contexts": [] },
  "enforce_admins": None,
  "required_pull_request_reviews": None,
  "restrictions": None})

        ghPATCHresponse = requests.put(ghRootEndpoint+protected_URL,payload,
                headers ={'Authorization':'token ' + ghAPIToken}).json()
        print(ghPATCHresponse)

    else:
        print("PERFECT")
    #print(getStatusCheckURL)




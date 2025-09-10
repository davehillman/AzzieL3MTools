## AzzieL3MTools
## runmain.py
## Hillman
## June 2025

import runl3m
import llmproc
from datetime import datetime
import utils

## this is a basic view for running LLMs (start, stop) and processing queries

llmfile = "config/llminit.json"

def initllms(llmitem):
    initstart = datetime.now()
    llmproc.setllmrun(llmitem)
    print("Total Init Time: " + str(datetime.now() - initstart))

def stopllms(llmitem):
    llmproc.stopllm(llmitem)


def runq(qry,exp):
    # initllms(llm)
    llmsel = utils.loadjson(llmfile)
    print("Running Query(ies)")
    sess_start = datetime.now()
    results =  runl3m.runquery(llmsel, qry,exp)
    time_str =  str(datetime.now() - sess_start)
    h,m,s = map(float, time_str.split(':'))
    total_seconds = h * 3600 + m * 60 + s
    print("Session Duration: " + str(total_seconds))
    return results


def getprompts():
    plist = utils.loadjson('config/llmprompts.json')
    pnames = []
    for i in plist:
        # pnames.append({i["preprompt"]["qryid"]: i["preprompt"]["qryname"]}) # dict
        pnames.append((i["preprompt"]["qryid"], i["preprompt"]["qryname"]))   #list, list
    return pnames


def getllmlist():
    return utils.loadjson('config/llminit.json')["llm"]["model"]    



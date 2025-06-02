## AzzieClassifier
## runmain.py
## Hillman
## June 2025

import runl3m
import llmproc
from datetime import datetime

## this is a basic view for running LLMs (start, stop) and processing queries

llmfile = "config/llminit.json"

def initllms():
    initstart = datetime.now()
    llmset = runl3m.loadjson(llmfile)["llm"]["model"]
    for i in llmset:
        llmproc.llmrun(i)
    print("Total Init Time: " + str(datetime.now() - initstart))
    # llmsel = runl3m.loadjson(llmfile)

def stopllms():
    llmset = runl3m.loadjson(llmfile)["llm"]["model"]
    for i in llmset:
        llmproc.stopllm(i)
    # llmsel = runl3m.loadjson(llmfile)

def runq(qry,exp):
    initllms()
    llmsel = runl3m.loadjson(llmfile)
    print("Running Query(ies)")
    sess_start = datetime.now()
    results =  runl3m.runquery(llmsel, qry,exp)
    time_str =  str(datetime.now() - sess_start)
    h,m,s = map(float, time_str.split(':'))
    total_seconds = h * 3600 + m * 60 + s
    print("Session Duration: " + str(total_seconds))
    return results


## AzzieL3MTools
## llmproc.py
## Hillman
## Jun 2025

import ollama
from datetime import datetime
import utils

## following loads the LLM data
llmfile = "llminit.json"

def initllm():
    global llmfile
    timestart = datetime.now()
    llmsel = utils.loadjson(llmfile)

    print("==>LLM Init Time: " + str(datetime.now() - timestart))
    return llmsel    

def llmrun(llm):
    print("Checking LLM status... " + llm)
    llmrunning = False
    for i in getcurrentllm():
        if  i["model"] == llm:
            llmrunning = True
            break
    if not llmrunning:
        print("Starting " + llm + ": " + startllm(llm,"30m")) 
    else:
        print(llm + " is RUNNING")  


def llmstop():
    if getcurrentllm() != []:
        getllm = getcurrentllm()[0]["model"]
        print("STOPPING: " + getllm)
        print(stopllm(getllm))
    else:
        print("No LLM is running.")

def getllmlist():
    lset= []
    lmlist = ollama.list()["models"]
    for i in lmlist:
        lset.append(i['model'])
    return lset 


def getcurrentllm():
    llmcurr = ollama.ps()["models"]
    curr = str(llmcurr)
    if curr.strip() == "": curr = "NO Models are currently running!"
    return llmcurr

def startllm(model,llmtime="30m"):
    try:
        print("Starting: " + model + " for " + llmtime)
        
        ollama.chat(model=model,keep_alive=llmtime,   messages=[
                {"role":"system",
                 "content":"Initialize" }
            ])
        return model + " ... STARTED"
    except:
        return model + " ... LOAD FAILED"
    return


def stopllm(model):
    try:
        ollama.chat(model=model, keep_alive=0)
        return model + " ... TERMINATED"
    except:
        return model + " ... TERMINATION FAILED"
    return


## use following when you want to stop all then run
def setllmrun(llm,kill=True):
    lset = getcurrentllm()
    for i in lset:
        stopllm(i["model"])
    if llm != "": 
        print(startllm(llm))
    else:
        print("ALL LLMs are stopped")



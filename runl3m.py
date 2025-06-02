## AzzieClassifier
## runl3m.py
## Hillman
## Jun 2025

import ollama
import json

## provides execution for query processing via the LLM

## file handling functions  follow (housekeeping)
keep_alive = "30m"

def loadjson(fname):
    with open(fname, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def loadtext (fname):
    with open(fname,"r") as file:
        return file.read()

## execution functions follow

def execllm(model,qrun, llmoptions,llmsystem):
    try:
        response = ollama.chat(
            model=model,
            stream=False,
            format="json",
            keep_alive= keep_alive,
            messages=[
                {"role":"system", "content": json.dumps(llmsystem) },
                {"role":"user","content":json.dumps(qrun)}
            ],
            options = llmoptions
        )
        resp = response["message"]["content"]
        return resp  
    except:
        print("Error detected")

## following gets the preprompt from the pp file
def getpreprompt(pp):
    pplist = loadjson("config/llmprompts.json")
    # fnd = False
    ipp = {"preprompt": {}}
    for i in pplist:
        if i["preprompt"]["qryid"] == pp: 
            ipp = i
    return ipp

## primary function for running the LLM

def runquery(llmsel, qry,exp):
    global keep_alive
    model = "hermes3:latest"
    pp = "class_milintel"
    if exp != "": pp = "class_milwexpl"

    llmoptions = llmsel["llm"]["setup"] 
    keep_alive = llmsel["llm"]["keep_alive"]
    
    pp = getpreprompt(pp)
    llmsystem = pp["preprompt"]["system"]

    results = execllm(model,qry, llmoptions,llmsystem)
    return results




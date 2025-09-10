## AzzieL3MTools
## runl3m.py
## Hillman
## Jun 2025

import ollama
import json
import parse
import utils
import llmproc

## provides execution for query processing via the LLM


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
    pplist = utils.loadjson("config/llmprompts.json")
    # fnd = False
    ipp = {"preprompt": {}}
    for i in pplist:
        if i["preprompt"]["qryid"] == pp: 
            ipp = i
    return ipp

## primary function for running the LLM

def runquery(llmsel, qry, pp):
    global keep_alive
    print(pp)
    model = llmproc.getcurrentllm()[0]["model"]

    llmoptions = llmsel["llm"]["setup"] 
    keep_alive = llmsel["llm"]["keep_alive"]
    
    fpp = getpreprompt(pp)
    llmsystem = fpp

    # results = execllm(model,qry, llmoptions,llmsystem)
    results = []
    
 
    if fpp["preprompt"]["proctype"] == "word":
        wordlist = parse.parse_to_wordlist(qry)
        print("run multiple, word")
        for i in wordlist:
            print(i)
            qrun = {}
            qrun["QUERY"] = i
            qrun["RESULTS"] = json.loads(execllm(model,i, llmoptions,llmsystem))
            results.append(qrun)
        return json.dumps(results,indent=4)
    elif fpp["preprompt"]["proctype"] == "line":
        qrylist = parse.runsentparsetolist(qry)
        print("run multiple, line")
        for i in qrylist:
            print(i)
            qrun = {}
            qrun["QUERY"] = i
            qrun["RESULTS"] = json.loads(execllm(model,i, llmoptions,llmsystem))
            results.append(qrun)
        return json.dumps(results,indent=4)
    elif fpp["preprompt"]["proctype"] == "doc":
        print("run document ")
        # for i in qrylist:
        print(qry)
        qrun = {}
        qrun["QUERY"] = qry
        qrun["RESULTS"] = json.loads(execllm(model,qry, llmoptions,llmsystem))
        results.append(qrun)
        return json.dumps(results,indent=4)





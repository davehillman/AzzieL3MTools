## AzzieL3MTools
## runl3m.py
## Hillman
## April 2026

import ollama
import json
import parse
import utils
import llmproc
from datetime import datetime
import httpx
import os
import jsonfix


BASE_URL = "https://ollama.com"


def chat_cloud(model:str, qrun: str, llmsystem,llmsettings):   # -> dict:
    API_KEY = os.getenv("OLLAMA_API_KEY")
    print("API Key for Ollama: ",API_KEY)  # use as a test to make sure it is available
    # if instruct == "": instruct = "You are a precise data analysis assistant. Return JSON only."
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": json.dumps(llmsystem)},
            {"role": "user", "content": json.dumps(qrun)},
        ],
        "stream": False,
        "format": llmsettings["format"],
       "options": {
           "temperature": llmsettings["options"]["temperature"], 
           "num_ctx": llmsettings["options"]["num_ctx"]
       },

    }

    with httpx.Client(timeout=180) as client:
        r = client.post(f"{BASE_URL}/api/chat", headers=headers, json=payload)
        r.raise_for_status()
        resp = utils.extract_json_from_markdown(r.json()["message"]["content"])
        print(utils.count_tokens(json.dumps(resp)) + utils.count_tokens(qrun))
        return resp


## provides execution for query processing via the LLM

## execution functions follow

def execllm(model:str, qrun: str, llmsystem,llmoptions):
    try:
        starttime = datetime.now()
        response = ollama.chat(
            model=model,
            stream=False,
            
            format= llmoptions["format"],
            keep_alive= llmoptions["keep_alive"],
            messages= [
                {"role":"system", "content": json.dumps(llmsystem) },
                {"role":"user","content":json.dumps(qrun)}
            ],
            options = llmoptions["options"]
        )
        resp = response["message"]["content"]

# following are used more status monitoring
        print(str(datetime.now() - starttime))
        print(utils.count_tokens(json.dumps(resp)) + utils.count_tokens(qrun))
        return jsonfix.parse_llm_json(resp) 
    except Exception as e:
        print("Error detected: ", e)
        return json.dumps({"output": "Error Detected, Probably a Failure of the LLM"})


## primary function for running the LLM
def rundata(model:str, qry:str, pp:str,llmset:str):
    global keep_alive

    runlocal = True
    if ":CLOUD" in model.upper():
        runlocal = False
    else:
        model = llmproc.getcurrentllm()   

    fpp = llmproc.getpreprompt(pp)
    llmsystem = fpp["preprompt"]["system"]  ## preprompt    
    
    llmoptions = llmproc.getllmsettings(llmset)  ## llmsettings
    results = []

    if fpp["preprompt"]["proctype"] == "word":
        wordlist = parse.parse_to_wordlist(qry)
        print("run multiple, word")
        for i in wordlist:
            qrun = {}
            qrun["QUERY"] = i
            if runlocal: 
                qrun["RESULTS"] = execllm(model,i.strip(), llmsystem, llmoptions)
            else:
                qrun["RESULTS"] = chat_cloud(model,i,llmsystem, llmoptions)
            results.append(qrun)
    elif fpp["preprompt"]["proctype"] == "line":
        qrylist = parse.runsentparsetolist(qry)
        print("run multiple, line")
        for i in qrylist:
            qrun = {}
            qrun["QUERY"] = i
            if runlocal: 
                qrun["RESULTS"] = execllm(model,i, llmsystem, llmoptions)
            else:
                qrun["RESULTS"] = chat_cloud(model,i,fpp, llmoptions)
            results.append(qrun)
    elif fpp["preprompt"]["proctype"] == "doc":
        print("run document")
        qrun = {}
        qrun["QUERY"] = qry       ## adds query text to output, can be commented out
        if runlocal: 
            qrun["RESULTS"] = execllm(model,qry, llmsystem, llmoptions)
        else:
            qrun["RESULTS"] = chat_cloud(model,qry,fpp, llmoptions)
        results.append(qrun)
    elif fpp["preprompt"]["proctype"] == "json":
        print("run json")
        qrun = {}
        if runlocal: 
            qrun["RESULTS"] = execllm(model,qry, llmsystem, llmoptions)
        else:
            qrun["RESULTS"] = chat_cloud(model,qry,fpp, llmoptions)
        results.append(qrun)
    utils.saveresults(results, model,pp)
    return json.dumps(results,indent=4)


# pull payload data from a file (text)
def getpayload(inval: str):
    payval = inval
    if "file:" in inval.lower():
        fname = inval[5:]
        payval = utils.loadtext(fname)
    return payval

def runbatch(fname: str):
    bdata = utils.loadjson(fname)
    llmset = bdata["llm"]
    if llmset[0] == "all_local":            
        llmset = llmproc.getlocalmodels()[0]
    platform = utils.get_system_info()
    llmsettings = bdata["llmsettings"]
    batch = bdata["batchrun"]
    savestats = bdata["savestats"]

    resfname = bdata["results"]
    # one file for each model
    resultset = []
    setinstructions = True
    for k in llmset:
        resdata = []

        llmconfig = {"llm_config": llmproc.getllmlist(k)}
        if llmconfig["llm_config"] == {}: break
        llmproc.startllm(k, llmproc.getllmsettings())
        resdata = [llmconfig]
         
        instructset = {}
        for i in llmsettings:
            llmsetup = llmproc.getllmsettings(i)
            
# each batch item is run for each setting above
            brun = []
            for j in batch:
                if j["active"] != "True": continue
                rundatasets = {}
                start = datetime.now()
                btype = j["type"]
                ppid = j["qryid"]
                pp = llmproc.getpreprompt(ppid)
                instructset[ppid] = pp
                payload = getpayload(j["payload"])
                payloadtokens = parse.count_tokens(json.dumps(payload))
                payloadbytes = len(json.dumps(payload).encode("utf-8"))
                queryres = rundata(k,payload,ppid,i)
                result_tokens = parse.count_tokens(json.dumps(queryres))
                result_size = len(queryres.encode("utf-8"))
                fintime = str(datetime.now() - start)
                jqueryres = json.loads(queryres)
                
                if savestats == "True": 
                    rundatasets = {
                            "run_type":btype,
                            "instructions": ppid,
                            "payload_tokens": payloadtokens,
                            "payload_bytes": payloadbytes,
                            "results_full": jqueryres,
                            "result_tokens": result_tokens,
                            "results_size": result_size,
                            "run_proctime": fintime
                        }
                else:
                    rundatasets = {
                        "results_full": jqueryres
                    }
                brun.append(rundatasets)
             
            resdata.append({"llm_settings": llmsetup, "batch_run": brun})

        llmproc.stopllm(k)
        if setinstructions: 
            if ":cloud" in k.lower(): platform = "Ollama (Web Remote)"
            resultset.append({"platform": platform})
            
            resultset.append({"instruction_set": instructset})
            setinstructions = False
        resultset.append(resdata)

        utils.savejson(resfname,resultset)
    return "Batch Complete"


def runproc(llm:str ,qry:str,pp:str,llmset:str,batch=""):
    print("LLM: ",llm, " ==>QRY: ",qry[0:30], "... ==>PP: ", pp, " ==>LLMset: ", llmset, " ==>BATCH: ", batch)
    if batch != "":
        results = runbatch(batch)
    else:
        results = [rundata(llm, qry,pp,llmset)]
    return results




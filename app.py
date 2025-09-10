## AzzieL3MTools
# ## app.py
## Hillman
## Jun 2025

from flask import Flask, request, render_template
import runmain
# import runl3m
import llmproc
import json
import random
import utils

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5000 * 1024 * 1024  # 200 MB

## Note: print functions have been used to output statuses and situations

# load and initialize the single web page
@app.route('/')
def index():
    return render_template('indexrun.htm')

# process query, return result
@app.route("/runquery",  methods=["POST"])
def runquery():
    if request.method == 'POST':
        # llm = request.form.get("llm")
        qry = request.form.get("qrydata")
        pp = request.form.get("pp")

    results = [runmain.runq(qry,pp)]   
    return json.dumps(results)

# load and initialize the LLM
@app.route("/initllm",  methods=["POST"])
def initllm():
    if request.method == 'POST':
        llmitem = request.form.get("llmsel")
    runmain.initllms(llmitem)
    results = "LLM Action Initiated"
    return json.dumps(results)

# stop the currently loaded llm 
@app.route("/stopllm",  methods=["POST"])

def stopllm():
    if request.method == 'POST':   
        llmitem = request.form.get("llmsel")
    runmain.stopllms(llmitem)
    results = "LLMs Stopped"
    return json.dumps(results)

# accesses and returns the sample queries (to support demos)
@app.route("/loadtest",  methods=["POST"])
def loadtest():
    tdata = utils.loadtext("config/milprompts.txt")
    tdset = tdata.split("\n")
    sel = random.randint(0, len(tdset) - 1)

    return json.dumps(tdset[sel])



## ---------------------------------------------------------
## configuration code

@app.route("/loadmodels",methods= ['GET','POST'])
def loadmodels():
    mset = runmain.getllmlist()
    return json.dumps(mset)

@app.route("/loadprompts",methods= ['GET','POST'])
def loadprompts():
    mset = runmain.getprompts()
    return json.dumps(mset)


@app.route("/getcurrentllm")
def getlcurrentllm():
    llmlist = llmproc.getcurrentllm()
    llmres = ""
    if isinstance(llmlist,list) and len(llmlist) > 0: llmres = llmlist[0]["model"]

    return json.dumps(llmres)


# run from port 15000
if __name__ == '__main__':
    app.run(port=15000,host='0.0.0.0', debug=True)
    
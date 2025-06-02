## AzzieClassifier
# ## app.py
## Hillman
## Jun 2025

from flask import Flask, request, render_template
import runmain
import runl3m
import json
import random

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
        qry = request.form.get("qrydata")
        exp = request.form.get("explain")

    results = [runmain.runq(qry,exp)]   
    return json.dumps(results)

# load and initialize the LLM
@app.route("/initllm",  methods=["POST"])
def initllm():
    runmain.initllms()
    results = "LLM Initialized"
    return json.dumps(results)

# stop the currently loaded llm 
@app.route("/stopllm",  methods=["POST"])
def stopllm():
    runmain.stopllms()
    results = "LLMs Stopped"
    return json.dumps(results)

# accesses and returns the sample queries (to support demos)
@app.route("/loadtest",  methods=["POST"])
def loadtest():
    tdata = runl3m.loadtext("config/milprompts.txt")
    tdset = tdata.split("\n")
    sel = random.randint(0, len(tdset) - 1)

    return json.dumps(tdset[sel])


# run from port 15000
if __name__ == '__main__':
    app.run(port=15000,host='0.0.0.0', debug=True)
    
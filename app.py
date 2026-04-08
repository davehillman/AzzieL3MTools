## AzzieL3MTools
# ## app.py
## Hillman
## March 2026


from flask import Flask, request, render_template
import runl3m
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

@app.route('/indexllmeval')
def indexllmeval():
    return render_template('indexllmeval.htm')

# process query, return result
@app.route("/runquery",  methods=["POST"])
def runquery():
    if request.method == 'POST':
        llm = request.form.get("llm")
        qry = request.form.get("qrydata")
        pp = request.form.get("pp")
        llmset = request.form.get("llmset")

    results = runl3m.runproc(llm, qry,pp,llmset,"")
    return json.dumps(results)

# load and initialize the LLM
@app.route("/initllm",  methods=["POST"])
def initllm():
    llmitem = ""
    if request.method == 'POST':
        llmitem = request.form.get("llmsel")

    if llmitem == "":
        stopllm()
    else:
        llmproc.startllm(llmitem)
    results = "LLM Action Initiated"
    return json.dumps(results)

# stop the currently loaded llm 
@app.route("/stopllm",  methods=["POST"])
def stopllm():
    if request.method == 'POST':   
        llmitem = request.form.get("llmsel")
    llmproc.stopllm(llmitem)
    results = "LLMs Stopped"
    return json.dumps(results)

# accesses and returns the sample queries (to support demos)
@app.route("/loadtest",  methods=["POST"])
def loadtest():
    pp = ""
    if request.method == 'POST':   
        pp = request.form.get("pp")
    fname = "nosel.txt"   
    ldir = "testdata/"
    docs = False
    if pp == "def_simple" or pp == "related_terms":
        fname = "defprompts.txt"
    elif pp == "class_milintel" or pp == "class_milwexpl":  
        fname = "milprompts.txt"      
    elif pp == "ask":
        fname = "askprompts.txt"
    elif pp == "eval_coa":
        fname = "coaprompts.txt"
    elif pp == "assess_trl":
        fname = "trlprompts.txt"
    elif pp == "eval_sent":
        fname == "sentprompts.txt"
    elif pp == "sum_docs" or pp == "ext_keywords" or pp == "sum_short":
        fname = "summprompts.txt"
        docs = True
    tdata = utils.loadtext(ldir + fname)
    tdset = tdata.split("\n")
    sel = random.randint(0, len(tdset) - 1)
    if docs == True:
        fsel = f"{ldir}files/{tdset[sel]}"
        tdata = utils.loadtext(fsel) 
    else:
        tdata = tdset[sel]   

    return json.dumps(tdata)



## ---------------------------------------------------------
## configuration code

@app.route("/loadmodels",methods= ['GET','POST'])
def loadmodels():
    mset = llmproc.getllmlist()
    return json.dumps(mset)

@app.route("/loadbatchfiles",methods= ['GET','POST'])
def loadbatchfiles():
    trlist = []
    trlist = utils.find_filenames_by_name("batch", "","json")
    return json.dumps(trlist)

@app.route("/loadbatchresults",methods= ['GET','POST'])
def loadbatchresults():
    trlist = []
    trlist = utils.find_filenames_by_name("batchres", "","json")
    return json.dumps(trlist)




@app.route("/getllmtestres",methods= ['GET','POST'])
def getllmtestres():
    if request.method == 'POST':   
        pp= request.form.get("mname")
    mset = utils.loadjson(pp)
    return json.dumps(mset)



@app.route("/loadsettings",methods= ['GET','POST'])
def loadsettings():
    mset = llmproc.getllmsetlist()
    return json.dumps(mset)

@app.route("/loadprompts",methods= ['GET','POST'])
def loadprompts():
    mset = utils.getprompts()
    return json.dumps(mset)


@app.route("/getcurrentllm")
def getlcurrentllm():
    llmlist = llmproc.getcurrentllm()

    return json.dumps(llmlist)

# gets info on the requested LLM
@app.route("/getllmdata",  methods=["POST"])
def getllmdata():
    if request.method == 'POST':   
        llmitem = request.form.get("mname")
    if llmitem == "": return json.dumps("")
    ldata = llmproc.getllmdata([llmitem])
    return json.dumps(ldata)

# gets info on the requested LLM
@app.route("/getbatchfile",  methods=["POST"])
def getbatchfile():
    if request.method == 'POST':   
        llmitem = request.form.get("mname")
    if llmitem == "": return json.dumps("")
    ldata = llmproc.getllmdata([llmitem])
    return json.dumps(ldata)


# gets info on the requested LLM
@app.route("/getsettingsdata",  methods=["POST"])
def getsettingsdata():
    if request.method == 'POST':   
        llmitem = request.form.get("mname")
    if llmitem == "": return json.dumps("")
    ldata = llmproc.getllmsettings(llmitem)

    return json.dumps(ldata)


# gets info on the requested prompt
@app.route("/getpromptdata",  methods=["POST"])
def getpromptdata():
    if request.method == 'POST':   
        pp= request.form.get("mname")
    if pp == "": return json.dumps("")
    ldata = runl3m.getpreprompt(pp)
    return json.dumps(ldata)

@app.route("/loadbatchfile", methods=["POST"])
def loadbatchfile():
    if request.method == 'POST':   
        item = request.form.get("edititem")
    if item == "": return json.dumps(["No File Selected"])
    fname = item
    return json.dumps(utils.loadjson(fname))


@app.route("/loadbatchresultsfile", methods=["POST"])
def loadbatchresultsfile():
    if request.method == 'POST':   
        item = request.form.get("edititem")
    if item == "": return json.dumps(["No File Selected"])
    fname = item
    return json.dumps(utils.loadjson(fname))

@app.route("/runbatch", methods=["POST"])
def runbatch():
    if request.method == 'POST':   
        item = request.form.get("edititem")
    if item == "": return json.dumps(["No File Selected"])
    fname = item
    status = runl3m.runproc("","","","",batch=fname)
    return json.dumps([status])




@app.route("/loadedititem", methods=["POST"])
def loadedititem():
    if request.method == 'POST':   
        item = request.form.get("edititem")
    if item == "": return json.dumps(["No File Selected"])
    fname = "config/" + item
    return json.dumps(utils.loadjson(fname))
    
@app.route("/saveeditsettings", methods=["POST"])
def saveeditsettings():
    if request.method == 'POST':   
        setdata = json.loads(request.form.get("setdata"))   
        edititem = request.form.get("edititem")
        fname = "config/" + str(edititem)
    utils.savejson(fname,setdata)
    return json.dumps(["Done"])

@app.route("/savebatchfile", methods=["POST"])
def savebatchfile():
    if request.method == 'POST':   
        setdata = json.loads(request.form.get("setdata"))   
        edititem = request.form.get("edititem")
    fname = str(edititem)
    utils.savejson(fname,setdata)
    return json.dumps(["Done"])


if __name__ == '__main__':
    app.run(port=15000,host='0.0.0.0', debug=True)
    
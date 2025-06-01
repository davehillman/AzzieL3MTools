===================================================================

AzzieClassifier Demonstration
developed by D. Hillman
June 2025

===================================================================

Introduction

This application is intended to demonstrate the viability and operation of a tool to classify text strings (sentences).  As this is available on commercial/open platforms, do not run real classified information.  Installing and running on classified systems should follow local and military/intel/government agency standards and protocols.

This application is designed to run on a CPU limited platform with a minimum of 16GB RAM (32 GB is recommended).

LLMs for this application should include the following features:
a.  Compatible with Ollama.
b.  7 to 9 billion parameters.
c.  Q4 quantitization.
d.  Tested instances include hermes3, qwen, granite, llama. 
e.  Please note the base set of parameters found in the config/llminit  Note that these parameters can be adjusted as needed.

What does this application do?

This application is intended to determine classification (top secret, secret, classified, and unclassified) based on EO13526 which is divided into a number of categories in including "plans and operations", "foreign governments", etc..

The application contains two prompt-based solutions:
a.  Basic: provides a classification level (e.g., "Secret") for a specific category (e.g., "plans and operations")
b.  Reason: adds an explanation based on how the LLM determined the results.  
The "basic" solution will typically run 3-5 seconds, while the "reason" solution will take 10-12 seconds.

Output is in JSON as key-value pairs.

How accurate are the classification results?

Classification is one of those things that can find itself defined by "you will know it when you see it".  It can be contextually dependent and there is a tendency to "over" and "under" classifiy depending on individuals and organizations.  For the purposes of this technology demonstration, we are using the EO1356 guidelines for classification which offers a categorical view of what things should (and should not be) classified based on the classic levels (i.e., Top Secret, Secret, etc.).  Depending on the organization and use of this tool, the prompting structure can be "tweeked" to enforce higher and lower classifications.  Additionally, other categories could be added to handle privacy and medical (e.g., HIPAA) categorizations to support classification.


===================================================================

Setup and Running Instructions

1.  Familiarize yourself with and install Ollama (https://ollama.com/download).  Ollama will include drivers and an local web server to handle API requests.

2.  Download the hermes3:latest LLM model (https://ollama.com/library/hermes3)
Note: you can download other models, but you will need to change the reference in llminit.json file (config directory).  Recommend using 7-9 B parameter models with Q4 compression (typically run 5-7 GB in size).

3.  Set up for the application:
a.  Set up a virtual environment for Python (recommend v. 3.11+)
b.  Install Flask library (pip install flask)
c.  Install Ollama library (pip install ollama)

4.  Run the application:
a.  On local machine: http://localhost:15000
b.  In a local network: http://192.168.XX.XX:15000 (XX is locally dependent)
c.  If you move to an operational web cloud and expect to support many users, you will want to consider running this as a wsgi (gateway) application via Apache.

5.  Using the application:
a.  Start the LLM (note: the LLM can be set up for local initialization up document load (via JavaScript)).
b.  Enter a query string in the Query input box or...
c.  Click on "Load Test Data" button to provide a randomly selected query (see config/milprompts.txt, you can add additional queries as desired).
d.  Click on "Run Query" button to enable processing; results will be displayed in the Results box.
e.  Optional: the "Explain" button will rerun the query and provide an explanation (this is configured in the llmprompts.json file (config directory))
f.  You can halt the LLM (and free up memory) -- this is optional and not required (it is currently set up to stop after 30 minutes from initial use).

NOTES:
1.  LLMs run in the background via the Ollama service.  If you do not start the service, it will be started as part of the first query that you run.  The response time will be longer for results (as much as 30-45 seconds).
2.  LMM initialization typically takes 10 to 30 seconds depending on the platform.
3.  First queries tend to be a bit slower (2X - 3X later runs).
4.  Typically, post initialization queries will run in 3-5 seconds for single sentence queries.



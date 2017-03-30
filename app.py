# flask
from flask import Flask
from flask import request

# nlp libs
# from stat_parser import Parser
import nltk

# others
import pprint
import json

app = Flask(__name__)

# pyStatParser
parser = Parser()

# initialize pretty printer
pp = pprint.PrettyPrinter(indent=4)

@app.route('/webhook', methods=['POST'])
def handler():   
    reqBody = request.get_json()
    
    # get user query
    resolvedQuery = reqBody['result']['resolvedQuery']
    
    # NLTK POS tagging 
    posSentence = nltk.pos_tag(nltk.word_tokenize(resolvedQuery))
    
    # NP-chunking using a tag pattern - refer to NLTK book chapter 7 for more details
    grammar = """NP: {<DT>?<RB.*>*<JJ.*>*<CD>?<NN.*>+}
        PP: {<IN><NP>}
        NP: {<NP><PP>}
        """
    rp = nltk.RegexpParser(grammar)
    result = rp.parse(posSentence)
    
    # extract noun phrases from tree
    returnText = "Important phrases\n"
    for subtree in result.subtrees():
        if subtree.label() == "NP": returnText += (str(subtree) + "\n")      
    
    # create api.ai response     
    response = {"speech": returnText, "displayText": returnText, "data": {}, "contextOut": [], "source": "GSMArena"}

    # a response HAS to be sent
    return json.dumps(response)
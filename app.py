# flask
from flask import Flask
from flask import request

# nlp libs
from stat_parser import Parser
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
#     print("POS Tagging: List of Tuples")
    posTags = nltk.pos_tag(nltk.word_tokenize(resolvedQuery))
    print(posTags)
    print(type(posTags))
    for tag in posTags: print(str(tag)) # or pp.pprint(posTags)
    
    # NP-chunking using a tag pattern
    grammar = """NP: {<DT>?<RB.*>*<JJ.*>*<CD>?<NN.*>+}
        PP: {<IN><NP>}
        NP: {<NP><PP>}
        """
    rp = nltk.RegexpParser(grammar)
    result = rp.parse(posTags)
    print(type(str(result)))
    print(result)
       
    # pyStatParser phrase structure parsing
#     print("\nParse Tree: ")
#     parseTree = parser.parse(resolvedQuery)
#     print(type(parseTree))
#     print(parseTree)
    
    # create api.ai response 
    speech = str(result)
    response = {"speech": speech, "displayText": speech, "data": {}, "contextOut": [], "source": "GSMArena"}

    # a response HAS to be sent
    return json.dumps(response)
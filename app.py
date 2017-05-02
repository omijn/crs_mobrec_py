import flask

import queryprocessor
import responses
import strings
import scraper
import gadata

# initialize stuff
app = flask.Flask(__name__)
sc = scraper.Scraper()
qp = queryprocessor.QueryProcessor()
db = responses.DBClient()
api_ai_res = responses.ApiAiResponse()

@app.route('/webhook', methods=['POST'])
def handler():
    req_body = flask.request.get_json()        
    query = req_body['result']['resolvedQuery']
    phone = req_body['result']['parameters']['phone'] if 'phone' in req_body['result']['parameters'] else ''
    intent = req_body['result']['metadata']['intentName']
    session_id = req_body['sessionId']
    
    if intent == strings.DEVICEINFO_INTENT:
        search_results = sc.ga_quicksearch(phone)
        api_ai_res.set(search_results, session_id)
        
    elif intent == strings.SEARCHPHONE_INTENT or intent == strings.FALLBACK_INTENT:        
        parameters = qp.process(query)
        search_results = sc.ga_phone_finder(parameters)
        api_ai_res.set(search_results, session_id)

    elif intent in strings.NEXT_INTENTS:        
        api_ai_res.next(session_id)
    
    elif intent in strings.PREV_INTENTS:
        api_ai_res.prev(session_id)
    
    return api_ai_res.get(session_id)    
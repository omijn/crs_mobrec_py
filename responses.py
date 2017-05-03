import json
import pymongo

class DBClient:
    """MongoDB client"""
    
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client['crs']
        self.coll = self.db['responses']
    
    def insert(self, search_results, current_index, session_id):
        """Upsert a new set of search results after a service request is made by a particular user."""
        
        self.coll.update_one(
            {
                'session_id': session_id
            },
            {
                '$set':
                    {
                        'session_id': session_id,
                        'search_results': search_results,
                        'current_index': current_index
                    }
            },
            upsert=True
        )
        
    def find_update_increment(self, increment, session_id):
        """Increment or decrement the current index (result to be displayed) of the list of search results. """
        
        doc = self.coll.find_one({'session_id': session_id})        
        new_index = (doc['current_index'] + increment) % len(doc['search_results'])        
        doc = self.coll.update_one(
            {
                'session_id': session_id
            },
            {   
                '$set':
                    {
                        'current_index': new_index                    
                    }
            }
        )        
        
    def fetch(self, session_id):
        """Retrieve search results for a particular user."""
        
        doc = self.coll.find_one({'session_id': session_id})        
        return doc

class ApiAiResponse:
    
    dbc = DBClient()
    
    def __init__(self):
        self.search_results = []
        self.session_id = 0
        self.current_index = 0
        self.speech = 'No results found.',
        self.displayText = 'No results found.',
        self.data = {},
        self.source = 'GSMArena'
    
    def set_speech(self, speech):
        """Speech setter method."""
        
        self.speech = speech

    def set_display_text(self, displayText):
        """Display text setter method."""
        
        self.displayText = displayText
    
    def set_data(self, displayText, link):
        """Data setter method."""
        
        self.data = {
            "facebook": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": displayText,
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": link,
                                "title": "View Device Specs"
                            }
                        ]
                    }
                }
            },
            "kik": {
                "type": "link",
                "url": link,
                "text": displayText
            },
#             "telegram": {

#             }
        }
        
    def __create_response(self, search_results, current_index):
        """Build api.ai response"""                
        
        current_result = search_results[current_index]
                
        speech = current_result['name'] + "\n\n" + current_result['description']
        displayText = current_result['name'] + "\n\n" + current_result['description']
        link = current_result['link']
        
        self.set_speech(speech)
        self.set_display_text(displayText)
        self.set_data(displayText, link)
    
    def next(self, session_id):
        """Switch to next phone result."""
        
        self.dbc.find_update_increment(1, session_id)        
    
    def prev(self, session_id):
        """Switch to previous phone result."""
        
        self.dbc.find_update_increment(-1, session_id)
        
    def set(self, search_results, session_id):
        """Store phone search results (either quicksearch/phone finder) in response object and database."""
        
        self.search_results = search_results
        self.current_index = 0
                
        self.dbc.insert(search_results, self.current_index, session_id)
    
    def get(self, session_id):
        """Return object containing only api.ai key-value pairs."""
        
        doc = self.dbc.fetch(session_id)
        search_results = doc['search_results']
        current_index = doc['current_index']
                
        self.__create_response(search_results, current_index)
            
        obj = {
            'speech': self.speech,
            'displayText': self.displayText,
            'data': self.data,
            'source': self.source
        }
        
        return json.dumps(obj)
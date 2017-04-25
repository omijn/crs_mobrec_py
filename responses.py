import json

class ApiAiResponse:
    
    def __init__(self):
        self.phones = []
        self.current_index = 0
        self.speech = 'No results found.',
        self.displayText = 'No results found.',
        self.data = {},
        self.source = 'GSMArena'        
    
    def set_speech(self, speech):
        self.speech = speech

    def set_display_text(self, displayText):
        self.displayText = displayText
    
    def set_data(self, displayText, link):
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
    #         "telegram": {

    #         }
        }
        
    def __create_response(self):
        """Build api.ai response"""                
        
        current_result = self.phones[self.current_index]
                
        speech = current_result['name'] + "\n\n" + current_result['description']
        displayText = current_result['name'] + "\n\n" + current_result['description']
        link = current_result['link']
        
        self.set_speech(speech)
        self.set_display_text(displayText)
        self.set_data(displayText, link)
    
    def next(self):
        """Switch to next phone result."""
        
        self.current_index = (self.current_index + 1) % len(self.phones)
    
    def prev(self):
        """Switch to previous phone result."""
        
        self.current_index = (self.current_index - 1) % len(self.phones)
        
    def set(self, phones):
        """Store phone search results (either quicksearch/phone finder) in response object."""
        
        self.phones = phones
        self.current_index = 0
    
    def get(self):
        """Return object containing only api.ai key-value pairs."""
        
        if self.phones:
            self.__create_response()
            
        obj = {
            'speech': self.speech,
            'displayText': self.displayText,
            'data': self.data,
            'source': self.source
        }
        
        return json.dumps(obj)
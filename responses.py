class ApiAiResponse:
    speech = 'speech'
    displayText = 'displayText'
    data = 'data'
    source = 'source'
        
    def __init__(self):              
        self.dict = {
            ApiAiResponse.speech: 'No results found.',
            ApiAiResponse.displayText: 'No results found.',
            ApiAiResponse.data: {},
            ApiAiResponse.source: 'GSMArena'
        }
    
    def format(self, speech, displayText, link):
        self.setSpeech(speech)
        self.setDisplayText(displayText)
        self.setData(displayText, link)
    
    def setSpeech(self, speech):
        self.dict[ApiAiResponse.speech] = speech                         

    def setDisplayText(self, displayText):
        self.dict[ApiAiResponse.displayText] = displayText    
    
    def setData(self, displayText, link):
        self.dict[ApiAiResponse.data] = {        
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
class ApiAiResponse:    
        
    def __init__(self):                      
        self.speech = 'No results found.',
        self.displayText = 'No results found.',
        self.data = {},
        self.source = 'GSMArena'
    
    def format_device_info(self, speech, displayText, link):
        self.set_speech(speech)
        self.set_display_text(displayText)
        self.set_data_device_info(displayText, link)
    
    def set_speech(self, speech):
        self.speech = speech                         

    def set_display_text(self, displayText):
        self.displayText = displayText    
    
    def set_data_device_info(self, displayText, link):
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
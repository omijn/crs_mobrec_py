# gsmarena.com
GA_BASE_URL = 'http://www.gsmarena.com/'
GA_QUICKSEARCH_URL = 'http://www.gsmarena.com/results.php3'
GA_QUICKSEARCH_URL_PARAM1 = 'sQuickSearch'
GA_QUICKSEARCH_URL_PARAM2 = 'sName'
GA_PHONEFINDER_URL = 'http://www.gsmarena.com/results.php3'

# beautiful soup
HTML_PARSER = 'html.parser'

# text-processing.com API
SENTIMENT_ENDPOINT = 'http://text-processing.com/api/sentiment/'

# api.ai
DEVICEINFO_INTENT = 'Request Device Specs'
SEARCHPHONE_INTENT = 'Constrain'
SEARCHPHONE_FOLLOWUP_NEXT_INTENT = 'Constrain - next'
SEARCHPHONE_FOLLOWUP_MORE_INTENT = 'Constrain - more'
SEARCHPHONE_FOLLOWUP_PREV_INTENT = 'Constrain - previous'
DEVICEINFO_FOLLOWUP_NEXT_INTENT = 'Request Device Specs - next'
DEVICEINFO_FOLLOWUP_MORE_INTENT = 'Request Device Specs - more'
DEVICEINFO_FOLLOWUP_PREV_INTENT = 'Request Device Specs - previous'
FALLBACK_INTENT = 'Default Fallback Intent'

NEXT_INTENTS = [SEARCHPHONE_FOLLOWUP_NEXT_INTENT, SEARCHPHONE_FOLLOWUP_MORE_INTENT, DEVICEINFO_FOLLOWUP_NEXT_INTENT, DEVICEINFO_FOLLOWUP_MORE_INTENT]
PREV_INTENTS = [SEARCHPHONE_FOLLOWUP_PREV_INTENT, DEVICEINFO_FOLLOWUP_PREV_INTENT]
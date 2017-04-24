import re
import nltk
import gadata
import scraper

class QueryProcessor:
    
    np_grammar = """        
            NP: {<DT>?<RB.*>*<CD>?<JJ.*>*<CD>?<NN.*>+}
            NP_C: {<NP><NP>}
            NP_P: {<NP>(<IN><NP>)+}        
            SHOULD: {<MD><VB>}
            NP_S: {(<NP>|<PRP>)<SHOULD><IN><NP>}
            NP_J: {(<NP>|<PRP>)?<SHOULD><RB.*>*<CD>?<JJ.*>+<CD>?}
        """
    
    def __spellcheck(self, query):
        """Correct obvious spelling mistakes."""
        
        return query
    
    def __preprocess(self, query):
        """Query preprocessing and clever hacks.
                
        -> Convert '"' (double quote) to 'inch'. 
                Example: '5"' becomes '5inch'.                
        -> Convert values like 32GB to 32 GB so that 32 is tagged as CD and GB as NN/NNP.
        -> Convert the word 'i' to 'I' so that we reduce the number of (unnecessary) noun phrases captured.
        -> Convert GB values to MB. 
                Example: 4 GB becomes 4096 MB.        
        """
        
#         named_entities = gadata.named_entities
#         for ne in named_entities: 
#             query = re.sub(r"\b" + ne + r"\b", ne.title(), query)
        query = re.sub(r"\"", r"inch", query)
        query = re.sub(r"(\d+(.\d+)?)\s*", r"\1 ", query)
        query = re.sub(r"\bi\b", r"I", query)
        query = re.sub(r"(\d+)\s*(gb|gig\w*)", 
                       lambda match: '{} MB'.format(int(match.group(1)) * 1024), 
                       query, flags=re.IGNORECASE)

#         query = self.__spellcheck(query)        
        
        return query            
    
    def __postag_query(self, query):
        """Use default nltk part-of-speech tagger to tag user query."""
        
        tagged_query = nltk.pos_tag(nltk.word_tokenize(query))
        return tagged_query
    
    def __parse_query(self, tagged_query, np_grammar):
        """Generate parse tree of the (tagged) user query using custom noun phrase grammar.
        
        This is called NP-chunking.
        Refer to chapter 7 of the NLTK book for more details: http://www.nltk.org/book/ch07.html
        """
        
        rgx_parser = nltk.RegexpParser(np_grammar)
        parse_tree = rgx_parser.parse(tagged_query)
        return parse_tree
    
    def __pull_NPs(self, parse_tree):
        """From the parse tree, pull out all the NP chunks of interest."""
        
        NPs_of_interest = ["NP", "NP_S", "NP_J", "NP_P", "NP_C"]
        return_text = ""
        noun_phrases = []
        
        for subtree in parse_tree.subtrees():
            if subtree.label() in NPs_of_interest:                
                noun_phrases.append(subtree)
        
        return noun_phrases
    
    def __extract_NPs(self, query):
        """From the cleaned up user query, extract useful noun phrases defined by grammar.
        
        NP_S captures phrases like, "the camera should be 13 mp"
        NP_J captures phrases like, "it should be cheap"
        """
        
        np_grammar = QueryProcessor.np_grammar
        
        tagged_query = self.__postag_query(query)                        
        parse_tree = self.__parse_query(tagged_query, np_grammar)
        noun_phrases = self.__pull_NPs(parse_tree)
        
        return noun_phrases
    
    def __extract_parameters(self, noun_phrases):
        """Look for relevant parameters in the captured noun phrases.
        
        tokens - list of words in a noun phrases
        phrase - noun phrase string
        bigrams - list of bigrams of noun phrase
        tags - list of POS tags of tokens
        
        Value based parameters are those that can be identified in the user query
        by simply checking whether their expected values exist in the query.
        
        For example, if we see the token 'Android' in an NP, we know that its parameter will be OS type.
        Value based parameters are of three types:
            - csv
            - radio
            - check
        
        General parameters are those that need to be first identified using some keywords.
        Only once the parameter is identified, its value is captured.
        
        For example, if we see the token 'RAM' in an NP, we look for patterns like '4 GB' or adjectives like 'high'.
        
        General parameters are of one type, but there are three ways to obtain their values:
            - using a regular expression
            - capturing an adjective (JJ) or adverb (RB)
            - using a list predefined values
        """
        
        parameters = {}
                
        params = gadata.parameters
        for noun_phrase in noun_phrases:
            np = noun_phrase.leaves()
            tokens = [tuple[0].lower() for tuple in np]
            phrase = ' '.join(tokens)
            bigrams = [' '.join(tuple) for tuple in list(nltk.bigrams(tokens))]
            tags = [tuple[1] for tuple in np]

            for param in params:
                if param['category'] == 'value':
                    for identifier in param['identifiers']:
                        if identifier in tokens or identifier in bigrams:
                            reference = param['reference']
                            if param['type'] == 'csv':                                                                
                                if reference in parameters:
                                    parameters[reference] += ',' + str(param['values'][identifier])
                                else:
                                    parameters[reference] = str(param['values'][identifier])                                    
                            elif param['type'] == 'radio':
                                parameters[reference] = str(param['values']['yes'])
                            elif param['type'] == 'check':
                                parameters[reference] = ''
                            
                            
                elif param['category'] == 'general':
                    for identifier in param['reference_identifiers']:
                        if identifier in tokens or identifier in bigrams:
                            reference = param['reference']
                            if 'pattern' in param:
                                regex = param['pattern']
                                match = re.search(regex, phrase)
                                if match:
                                    parameters[reference] = match.group(0)
                                    break                                                                           

                            if 'pos' in param:
                                # if pos in tags
                                for pos in param['pos']:
                                    if pos in tags:
                                        lingvar = tokens[tags.index(pos)]
                                        parameters[reference] = lingvar
    #                             break

                            if 'values' in param:
                                if param['type'] == 'radio':
                                    parameters[reference] = str(param['values']['yes'])
                                else:
                                    for val in param['values']:
                                        if val in tokens:
                                            parameters[reference] = str(param['values'][val])
                                            break
                            
            print tokens
            print tags
            print
            
        return parameters
    
    def __resolve_params(self, parameters):
        """Resolve linguistic variables in parameters to explicit values."""
        
        return parameters
        
    def __phone_search(self, parameters):
        """Call GSMArena scraper."""
        
        sc = scraper.Scraper()
        phones = sc.ga_phone_finder(parameters)
        return phones
      
    def process(self, query):
        """Main class method."""
        
        query = self.__preprocess(query)
        noun_phrases = self.__extract_NPs(query)
        parameters = self.__extract_parameters(noun_phrases)
        print(parameters)
        parameters = self.__resolve_params(parameters)
        phones = self.__phone_search(parameters)
        return phones
#================================================================================================
# Tafadzwa Pasipanodya
# SYE: Python module for a sentence data structure
# 1/31/14
#================================================================================================
class sentence(object):
    '''
    This module is a sentence data structure
    '''

    #-------------------------------------------------------------------------------------------
    # The Construtor
    #-------------------------------------------------------------------------------------------
    def __init__(self, docName, stemmedWords, OGwords):
        '''
         Parameters: 1. docName is the name of the document to which this sentence belongs
                     2. stemmedWords is a list containing this sentence's words in stemmed form
                     3. OGwords is a list containing this sentence's words in their original form
         Preconditions: 1. type(docName) == str and docName != None
                        2. type(stemmedWords) == str and stemmedWords != None
                        3. type(OGwords) == str and OGwords != None
        '''
        self.stemmedWords = stemmedWords
        self.docName = docName
        self.OGwords = OGwords
        self.wordFrequencies = self.sentenceWordFreqs()
        self.lexRankScore = None


    #------------------------------------------------------------------------------------------
    # Accessor methods
    #------------------------------------------------------------------------------------------
    def getStemmedWords(self):
        '''
        Get this sentence's words in stemmed form
        '''
        return self.stemmedWords

    def getDocName(self):
        '''
        Get this name of the document to which this sentence belongs
        '''
        return self.docName
    
    def getOGwords(self):
        '''
        Get this sentence's words in their original form
        '''
        return self.OGwords

    def getWordFreqs(self):
        '''
        Get a dictionary of the word frequencies in this sentence
        '''
        return self.wordFrequencies
    
    def getLexRankScore(self):
        '''
        Get this sentence's LexRank score
        '''
        return self.LexRankScore
    
    def setLexRankScore(self, score):
        '''
        Method to set this sentence's LexRank score
        '''
        self.LexRankScore = score

        
    #-------------------------------------------------------------------------------------------
    # Method to build a dictioary of word frequencies for this sentence
    #-------------------------------------------------------------------------------------------
    def sentenceWordFreqs(self):
        '''
        Set up a word frequency dictionary for this sentence
        '''
        wordFreqs = {}
        for word in self.stemmedWords:
            if word not in wordFreqs.keys():
                wordFreqs[word] = 1
            else:
                wordFreqs[word] = wordFreqs[word] + 1
                
        return wordFreqs

    

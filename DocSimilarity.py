#===========================================================================================================================
# Tafadzwa Pasipanodya
# Computer Science SYE
# Python Module to provide sentence comparison functionality for a multi-document summarization application
#===========================================================================================================================

import nltk
import os
import math
import TextProcessing

class DocSimiliarity(object):
    #------------------------------
    # The class Construtor
    #------------------------------
    def __init__(self):
        self.text = TextProcessing.TextProcessing()
        
    #-----------------------------------------------------------------------------------------------------------------------
    # Method to compute the TF-IDF values for all words in a document cluster
    #
    # Preconditions: 1. type(sentences) == list-of-sentence #this is a list of sentence objects. Please check sentence object
    #                                                       #documentation for more information
    #
    # Returns: dict-of-word-float - this is the dictionary mapping every word to a Term frequency
    #-----------------------------------------------------------------------------------------------------------------------
    def TFs(self, sentences):
        # method variables
        tfs = {}
        
        # every sentence
        for sent in sentences:
            wordFreqs = sent.getWordFreqs()
            
            # every word
            for word in wordFreqs.keys():
                if tfs.get(word, 0) != 0:
                    tfs[word] = tfs[word] + wordFreqs[word]
                else:
                    tfs[word] = wordFreqs[word]
        return tfs
            
            
    #-----------------------------------------------------------------------------------------------------------------------
    # Method to compute the term frequency for a word in a given sentence
    #
    # Preconditions: 1.) type(word) == string and type(sentence) == sentence #this is the sentene data structure#
    #
    # Returns: the term frequency -> int
    #-----------------------------------------------------------------------------------------------------------------------
    def TFw(self, word, sentence):
        return sentence.getWordFreqs().get(word, 0)

    
    #-----------------------------------------------------------------------------------------------------------------------
    # Method to compute the IDF value of a given word
    #
    # Preconditions: 1.) type(word) == String (word is a stemmed word)
    #                2.) type(sentences) == list #this is a list of sentence data structures#
    #                3.) word != None and sentences != None
    #
    # Returns: dict-of-str-&-float #this is the dictionary of word -> idf-value for all the words in our cluster
    #-----------------------------------------------------------------------------------------------------------------------
    def IDFs(self, sentences):
        
        N = len(sentences)
        idf = 0
        idfs = {}
        words = {}
        w2 = []
        
        # every sentence in our cluster
        for sent in sentences:
            
            # every word in a sentence
            for word in sent.getStemmedWords():

                # dont calculate a word's IDF value more than once
                if sent.getWordFreqs().get(word, 0) != 0:
                    words[word] = words.get(word, 0)+ 1
                    
                    
        for word in words:
            n = words[word]
            # avoid zero division errors
            try:
                w2.append(n)
                idf = math.log10(float(N)/n)
            except ZeroDivisionError:
                idf = 0
                    
            # reset variables
            idfs[word] = idf
                
        return idfs

    #--------------------------------------------------------------------------------------------------------------------
    # Method to calculate the IDF values for all the words in a document cluster
    #
    # Preconditions: 1. type(word) == str #this is the word whose IDF value we want to find
    #                2. type(idfs) == dict-of-str-&-float #this is the dictionary of all the word's IDF values
    #
    # Returns: float - the word's idf value
    #--------------------------------------------------------------------------------------------------------------------
    def IDF(self, word, idfs):
        return idfs[word]


    #----------------------------------------------------------------------------------------------------------------------
    # Method to compute the similarity score between 2 sentences
    #
    # Preconditions: 1.) type(sent1) == sentence #this is a sentence object for our sentence#
    #                2.) type(sent2) == sentence #this is a sentence object for our query. a query is just a list of words#
    #                3.) Ttype(sentences) == list-of-sentence. #this is a list of all the sentences in our cluster# 
    #
    # Returns:  float - The similarity between the sentence and the document
    #----------------------------------------------------------------------------------------------------------------------
    def sim(self, sentence1, sentence2, idfs):
        # funcrion data
        numerator = 0
        denom1 = 0
        denom2 = 0

        # calculate the numerator first
        for word in sentence2.getStemmedWords():
            numerator += self.TFw(word, sentence2) * self.TFw(word, sentence1) * self.IDF(word, idfs) ** 2

        # calculate the denominator next  
        for word in sentence1.getStemmedWords():
            denom2 += (self.TFw(word, sentence1) * self.IDF(word, idfs)) ** 2
                
        for word in sentence2.getStemmedWords():
            denom1 += (self.TFw(word, sentence2) * self.IDF(word, idfs)) ** 2

        # calculate the similarity score last  
        try:
            return numerator / (math.sqrt(denom1) * math.sqrt(denom2))
        
        # just in case some bug led to a zero error (should be impossible)
        # but just make sure program doesn't crash
        except ZeroDivisionError:
            return float("-inf")


    

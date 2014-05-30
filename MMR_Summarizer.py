#===================================================================================================
# Tafadzwa Pasipanodya
# Computer Science SYE
# Python module to provide summary building functionality. Module uses a Maximum Marginal Relevance
#   algorithim to select the best n sentences in a document clusters
# November 2013
#===================================================================================================

import DocSimilarity
import os
import math
import TextProcessing
import sentence

class MMR_Summarizer(object):
    #---------------------
    # The Construtor
    #---------------------
    def __init__(self):
        self.text = TextProcessing.TextProcessing()
        self.sim = DocSimilarity.DocSimiliarity()


    #-------------------------------------------------------------------------------------------------
    # Method to compute every word's TF.IDF value in a given cluster
    #
    # Preconditions: 1. type(sentences) == list-of-sentence #Check sentence module for more information
    #                2. type(idfs) == dict-of-str-&-float #This is the dictionary word -> IDF value
    #               
    # Returns: dict-of-float-&-list-of-str - this is the dictionary {TF.IDF : [words]} for every word in the given
    #           cluster
    #--------------------------------------------------------------------------------------------------
    def TF_IDF(self, sentences, idfs):
        # Method variables
        tfs = self.sim.TFs(sentences)
        
        retval = {}

        # for every word
        for word in tfs:
            #calculate every word's tf-idf score
            tf_idfs=  tfs[word] * idfs[word]
            
            # add word and its tf-idf score to dictionary
            if retval.get(tf_idfs, None) == None:
                retval[tf_idfs] = [word]
            else:
                retval[tf_idfs].append(word)

        return retval


    #--------------------------------------------------------------------------------------------------
    # Method to build a query by selecting n words with the highest TF.IDF values
    #
    # Preconditions: 1. type(n) == int #n is the number of "best" words to include in our query
    #                2. type(sentences) == list-of-sentence # a sentence is a sentence object. Please check
    #                                                       # sentence object documentation#
    #                3. type(idfs) == dict-of-str-&-float #This is the dictionary word -> IDF value
    #
    # Returns: sentence object - a sentence object with n of the best words in a document cluster
    #--------------------------------------------------------------------------------------------------
    def makeQuery(self, n, sentences, idfs):
        scored_words = self.TF_IDF(sentences, idfs)
        best_words = self.getBestWords(n, scored_words)
        return sentence.sentence("query", best_words, [])


    #--------------------------------------------------------------------------------------------------
    # Method to build a list of the n best words in a cluster
    #
    # Precondition: 1. type(n) == int #n is the number of "best" words to include in our query
    #               2. type(scored_words) == dict-of-list-of-str #This is the dictionary of scored wors
    #
    # Returns: list-of-str #The list of n best words
    #--------------------------------------------------------------------------------------------------
    def getBestWords(self, n, scored_words):
        #local variables
        best_scores  = scored_words.keys()
        best_scores.sort()
        best_words = []

        # loop through the list in reverse order
        for i in range(-1, -n, -1):
            
            words = scored_words[best_scores[i]] #returns a list of words
            for word in words:
                if i >-n:
                    best_words.append(word)
                    i = i-1
        return best_words


    #----------------------------------------------------------------------------------------------------
    # Method to get the single Best matching sentence
    #
    # Preconditions: 1. type(sentences) == list-of-sentence. data is our entire cluster, compiled into a
    #                   single document
    #                2. type(query) == sentence. #Check sentence module for more information
    #                3. type(idfs) == dict-of-str-&-float # this is the dictionary word -> IDF value
    #              
    # Returns: a sentence object
    #----------------------------------------------------------------------------------------------------
    def getBestSentence(self, sentences, query, idfs):
        # variables to help keep track of the best file
        best_sent = None
        prev = float("-inf")
        
        # loop through all sentences
        for sent in sentences:
            similarity = self.sim.sim(sent, query, idfs)

            # take note of the best matching sentence
            if similarity > prev:
                best_sent = sent
                prev = similarity
                    
        # select the chosen best matching sentence from original data
        sentences.remove(best_sent)
        return best_sent


    #-------------------------------------------------------------------------------------------------------
    # Method to find n sentences with the best MR values
    #
    # Preconditions: 1. type(gamma) == float and gamma < 1 #this is our parameter to determine the relevance
    #                                                      #of a sentence
    #                2. type(sentences) == list-of-sentence #Check sentence module for more information
    #                4. type(query) == sentence    
    #                5. type(idfs) == dict-of-str-&-float   #this is the dictionary word -> IDF value
    #                5. type(summary_length) == int         #this is the desired length of our summary
    #                6. type(best_sentence) == sentence.    #the best sentence in our cluster
    #
    # Returns: list-of-sentence with summary_length-1 sentences
    #--------------------------------------------------------------------------------------------------------
    def makeSummary(self, gamma, sentences, query, best_sentence, idfs, summary_length ):
        # local variables
        selected_sentences = [best_sentence]
        summary = [best_sentence]
        
        for i in range(summary_length):
            best_line = None
            prev = float("-inf")
            
            # go through all sentences
            for sent in sentences:
                    
                # get the marginal relevance of a query
                curr = self.MR(gamma, sent, query, idfs, selected_sentences)
                    
                # set this sentence as the next best sentence if its' marginal releveance is better than the
                # current best
                if curr > prev:
                    prev = curr
                    best_line = sent
                    
            # update our selected sentences and summary            
            selected_sentences += [best_line]
            sentences.remove(best_line)
            
        return selected_sentences
            
            
    #--------------------------------------------------------------------------------------------------------
    # Method to compute the MR value for a given sentence
    #
    # Preconditions: 1. type(gamma) == float and 0< gamma < 1 # This is our parameter to determine the relevance
    #                                                         #     of a sentence
    #                2. type(sent) == sentence                # A sentence whoseMR we want to find. check sentence
    #                                                         #     module documentation
    #                3. type(query) == list-of-words          # This is a sentence consisting of words with the best
    #                                                         #     TF.IDF Values from our cluster
    #                4. type(idfs) == dict-of-str-&-float.    # This is the dict word -> IDF value
    #                5. type(selected_sentences) == list-of-stentence #This is the list of the currently selected
    #                                                                 #  sentences.
    #
    # Returns: A float. (this is the MR value for our sentence)
    #---------------------------------------------------------------------------------------------------------
    def MR(self, gamma, sent, query , idfs, selected_sentences):
        
        left_of_minus = gamma * self.sim.sim(sent, query, idfs)
        
        right_values = [float("-inf")]
        
        for selected_sentence in selected_sentences:
            right_values.append( (1 - gamma) * self.sim.sim(sent, selected_sentence, idfs))
            
        right_of_minus = max(right_values)
        
        return left_of_minus - right_of_minus

        
    #--------------------------------------------------------------------------------------------------------
    # Method to make a summary.
    #
    # Preconditions: 1. type(n) == int #this is the desired query length#
    #                2. type(summary_lenth) == int #this is the desired summary length#
    #                3. type(cluster_path) == str #this is the desired path to the document cluster#
    #
    # Returns: str - a summary of documents in the given cluster
    #--------------------------------------------------------------------------------------------------------
    def main(self, n, summary_lentgh, cluster_path):

        # open all files in the user specified directory
        sentences =  self.text.openDirectory(cluster_path)
        idfs = self.sim.IDFs(sentences)
       
        # build a query
        query = self.makeQuery(n, sentences, idfs)
        
        # pick a sentence that best matches our query
        
        best_sentence = self.getBestSentence(sentences, query, idfs)
        
        # build a summary by adding more relevant sentences
        summary = self.makeSummary(0.5, sentences, query, best_sentence, idfs, 4)
        
        return summary


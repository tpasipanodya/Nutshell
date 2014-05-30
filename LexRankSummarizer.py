#================================================================================================================
# Tafadzwa Pasipanodya
# SYE
# Python module to build a summary using the LexRank algorithm to select the best n sentences in a cluster of
#   documents
# 1/31/14
#================================================================================================================

import DocSimilarity
import os
import math
import TextProcessing
import sentence
import numpy
import copy

class LexRankSummarizer(object):
    
    #---------------------
    # The Construtor
    #---------------------
    def __init__(self):
        self.text = TextProcessing.TextProcessing()
        self.sim = DocSimilarity.DocSimiliarity()
        
    #-------------------------------------------------------------------------------------------------------------
    # Method to Generate the LexRank scores for sentences in a cluster of documents. this method updates and sets
    #   every sentence's LexRank score
    #
    # Preconditions: 1. type(sentences) == list-of-sentence # Check sentence module documentation for more
    #                       information
    #                2. type(idfs) == dict-of-str-&-float   # This is the dictionary word -> IDF value
    #                3. type(CM) == list-of-list-of-float   # This is our cosine matrix
    #                4. type(t) == float                    # this is a threshold measurement
    #
    # Returns: list-of-sentences. # the LexRankScore property has been updated
    #------------------------------------------------------------------------------------------------------------
    def score(self, sentences, idfs, CM, t):
        # local variables
        Degree = [0 for i in sentences]
        L = [0 for i in sentences]
        n = len(sentences)
        
        for i in range(n):
            for j in range(n):
                CM[i][j] = self.sim.sim(sentences[i], sentences[j], idfs)
                
                if CM[i][j] > t:
                    CM[i][j] = 1
                    Degree[i] += 1
                    
                else:
                    CM[i][j] = 0

        for i in range(n):
            for j in range(n):
                CM[i][j] = CM[i][j]/float(Degree[i])
                
        L = self.PowerMethod(CM, n, 0.2)
        normalizedL = self.normalize(L)
        
        for i in range(len(normalizedL)):
            score = normalizedL[i]
            sentence = sentences[i]
            sentence.setLexRankScore(score)
            
        return sentences

    #----------------------------------------------------------------------------------------------------------
    # Helper Method to generate an array of lex ranks, given a cosine matrix
    #
    # Preconditions: 1. type(CM) == list-of-list-of-float  # This is our cosine matrix of sentence scores
    #                2. type(n) == int                     # This is the number of sentences in our cluster
    #                    
    #                3. type(e) = float                    # This is our error threshold.
    #
    # Returns: an array of of lex ranks
    #----------------------------------------------------------------------------------------------------------
    def PowerMethod(self, CM, n, e):
        Po = numpy.array([1/float(n) for i in range(n)])
        t = 0
        delta = float('-inf')
        M = numpy.array(CM)
  
        while delta < e:
            t = t + 1
            M = M.transpose()
            P1 = numpy.dot(M, Po)
            diff = numpy.subtract(P1, Po)
            delta = numpy.linalg.norm(diff)
            Po = numpy.copy(P1)
            
        return list(Po)


    #---------------------------------------------------------------------------------------------------------
    # Method to build a matrix exhibiting all possible sentence combinations from our dataset
    #
    # Preconditions: type(sentences) == list-of-sentence # Check sentence module documentation for more
    #                                                    #  information
    # Returns: list-of-list-of-float # this is our N*N matrix. values are initially set to 0
    #---------------------------------------------------------------------------------------------------------
    def buildMatrix(self, sentences):

        # build our matrix
        CM = [[0 for s in sentences] for s in sentences]
        
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                CM[i][j] = 0
        return CM


    #--------------------------------------------------------------------------------------------------------
    # Method to build a summary using the LexRank algorithm
    #
    # Preconditions: 1. type(sentences) == list-of-sentence # This is the the list of sentences with updated
    #                                                       #   LexRank scores
    #                2. type(n) == int                      # this is our desired summary lenth
    #--------------------------------------------------------------------------------------------------------
    def buildSummary(self, sentences, n):
        sentences = sorted(sentences,key=lambda x: x.getLexRankScore(), reverse=True)
        summary = []
        for i in range(n):
            summary += [sentences[i]]
        return summary

        
    #--------------------------------------------------------------------------------------------------------
    # Method to normalize a list of numbers
    #
    # Preconditions: type(numbers) == list-of-int or type(numbers) == list-of-float # This is our list of numbers
    #                                                                                   to be normalized
    #
    # Returns: list-of-float. # This is a new list, where values in the original list are normalized between 0
    #                         #     and 1
    #--------------------------------------------------------------------------------------------------------
    def normalize(self, numbers):
        max_number = max(numbers)
        normalized_numbers = []
        
        for number in numbers:
            normalized_numbers.append(number/max_number)
            
        return normalized_numbers
    
    #--------------------------------------------------------------------------------------------------------
    # The main method to process inputs and build a summary
    #--------------------------------------------------------------------------------------------------------
    def main(self, n, path):
        sentences  = self.text.openDirectory(path)
        idfs = self.sim.IDFs(sentences)
        CM = self.buildMatrix(sentences)
    
        sentences = self.score(sentences, idfs,CM, 0.1)

        summary = self.buildSummary(sentences, n)

        return summary
    
        
        
        

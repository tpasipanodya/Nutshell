#=======================================================================================================
# Tafadzwa Pasipanodya
# Computer Science SYE
# Module provides file I/O functionality for a document summarizer
#=======================================================================================================

import nltk
import os
import math
import string
import sentence

class TextProcessing(object):

    #----------------------------------------------------------------------------------------------------
    # Method for file IO processes. Opens a file, Removes HTML tags and tokenizes the file
    #
    # Preconditions: 1.) file_path_and_name != None
    #                2.) type(file_path_and_name) == str
    #                3.) file_path_and_name is a valid file address in the file system
    #
    # Returns: 1. A list of sentence objects the sentence object has an empty sentence if file 404
    #----------------------------------------------------------------------------------------------------
    def processFile(self, file_path_and_name):
        try:
            # open file
            f = open(file_path_and_name,'r')
            text = f.read()

            # remove HTML tags
            text = nltk.clean_html(text.replace('\n', ''));

            # segement data into a list of sentences
            sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
                
            lines = sent_tokenizer.tokenize(text.strip())

            # ensure names used are in their complete form
            # text = self.use_full_names(lines)
            text = lines

            # convert sentences to list of words
            sentences = []
            porter = nltk.PorterStemmer()
            
            # every sentence
            for sent in lines:
                OG_sent = sent[:]
                sent = sent.strip().lower()
                line = nltk.word_tokenize(sent)
            
                # convert words to stemmed words before appending to list and returning
                stemmed_sentence = [porter.stem(word) for word in line]
                stemmed_sentence = filter(lambda x: x!='.'and x!='`'and x!=','and x!='?'and x!="'"
                                    and x!='!' and x!='''"''' and x!="''" and x!="'s", stemmed_sentence)
                # no empy sentences
                if stemmed_sentence != []:
                    sentences.append(sentence.sentence(file_path_and_name, stemmed_sentence, OG_sent))
            
            return sentences

        
        # print error message if file not found
        except IOError:
            print 'Oops! File not found',file_path_and_name
            return [sentence.sentence(file_path_and_name, [],[])]

    #-------------------------------------------------------------------------------------------------------
    # Method to process a document by replacing all versions of a name with the fullest version of the same
    # name.
    #
    # Preconditions: 1. type(doc) == list-of-str. Each string is a sentence.
    #
    # Returns: a list-of-str. Each string is a sentence
    #-------------------------------------------------------------------------------------------------------
    def use_full_names(self, doc):
        names = self.getNames(doc)
        
        for i in range(len(doc)):
            doc[i] = self.getLongName(doc[i], names)
        return doc
        

    #----------------------------------------------------------------------------------------------------------
    # Method to get all the named entities in a document
    #
    # Preconditions: 1. type(doc) == list-of-str. This document is a list of sentences. A sentence is a string
    #
    # Returns: a list-of-str. Each sting in our list is a full version of a name
    #----------------------------------------------------------------------------------------------------------
    def getNames(self, doc):
        # join sentences into one long string and split it into a list of words
        doc = ' '.join(doc).split()
        # load the stanford named entity classifier
        st = nltk.tag.stanford.NERTagger('C:/Users/tmpasi10/Desktop/ner/classifiers/english.all.3class.distsim.crf.ser.gz',\
                                         'C:/Users/tmpasi10/Desktop/ner/stanford-ner.jar')
        # get the nouns
        tags = st.tag(doc)# just a list of names. each name is a tupple
        doc = ' '.join(doc)

        names = []

        flag1 = False # is this a 3 part name eg John Peter Smith or Elizabeth Stella Doe

        # build a list of known complete names
        for i in range(1, len(tags)):
            tag1 = tags[i-1]
            tag2 = tags[i]
            
            if i+1 < len(tags):
                tag3 = tags[i+1]
                if tag1[1] == 'PERSON' and tag2[1] == 'PERSON' and tag3[1] =='PERSON':
                    name = tag1[0] + ' ' + tag2[0] + ' ' + tag3[0]
                    if doc.find(name) > -1:
                        names.append(name)
                        i = i + 3
                        flag1 = True

            if tag1[1] == 'PERSON' and tag2[1] == 'PERSON' and not flag1 and i<len(tags):
                name = tag1[0] + ' ' + tag2[0]
                if doc.find(name) > -1:
                    names.append(name)
                    i = i + 2
                else:
                    i = i + 1
        return names

    #---------------------------------------------------------------------------------------------------------
    # Method to replace all shortened versions of a name with their original long version
    #
    # Preconditions: 1. type(sentence) = list-of-str and type(names) = list-of-str
    #                2. sentence != None and names != None
    #
    # Returns: a string. The sentence is joined into a string and returned after name replacement operations
    #           are completed
    #---------------------------------------------------------------------------------------------------------
    def getLongName(self, sentence, names):
        sentence = sentence.split(" ")
        
        i = 0
        while i < len(sentence):
            word1 = sentence[i]
            for name in names:
                flag = False

            # check 2 words at a time
                if i+1 != len(sentence):
                    word2 = sentence[i+1]
                    _2words = word1 + ' ' + word2
                    if self.begins_or_ends_with(_2words, name) and _2words != name:
                        if i == len(sentence)-2:
                            print sentence[i-1] + ' ' +_2words, name
                            sentence[i] = name
                            sentence = sentence[:i] + [name]
                            flag = True
                           
                        else:
                            temp = _2words + ' ' + sentence[i+2]
                            if temp != name and temp[:len(temp)-1] != name:
                                sentence = sentence[:i] + [name] + sentence[i+2:]
                                flag = True
                                
            # check one word at a time
                if self.begins_or_ends_with(word1, name) and not flag:
                    if i == len(sentence)-1:
                        sentence[i] = name
                       
                    else:
                        if sentence[i+1] != name.split(" ")[1]:
                            sentence[i] = name
            i +=1          
                        
        return ' '.join(sentence)

    #---------------------------------------------------------------------------------------------------------
    # Method to check whether a word is part of the begining or ending of a recognized name
    #
    # Preconditions: 1. type(word) == str and type(name) == str
    #                   word is always any word from a sentence. name is a complete version of a name, eg
    #                   word = 'Jane', name = 'Jane Doe'
    #
    # Returns: a Boolean
    #---------------------------------------------------------------------------------------------------------
    def begins_or_ends_with(self, word, name):
        return name[:len(word)] == word or name[len(name)-len(word):] == word


    #--------------------------------------------------------------------------------------------------------
    # Method to get a document's file path
    #
    # Preconditions: 1. file_name refers to a document in the same parent directory as TextProcessing.py
    #                   i.e,  file_name is one level deeper than TextProcessing.py in the directory path hierachy
    #                2. type(file_name) == str and file_name != None
    #
    # Returns: a string; the filepath to the file file_name
    #--------------------------------------------------------------------------------------------------------
    def get_file_path(self, file_name):
        for root, dirs, files in os.walk(os.getcwd()):
            for name in files:
                if name == file_name:
                    return os.path.join(root,name)
        print "Error! file was not found!!"
        return ""
    
    #--------------------------------------------------------------------------------------------------------
    # Method to get all file names from a directory
    #
    # Prenditions: 1.) path is the directory path in string format
    #              2.) path is not None
    #
    # Returns: a list of all file paths in a directory
    #--------------------------------------------------------------------------------------------------------
    def get_all_files(self, path = None):
        retval = []
        
        # use current directory if no path given
        if path == None:
            path = os.getcwd()

        # get all files in the given directory
        for root, dirs, files in os.walk(path):
            for name in files:

             # make sure we arent considering code files as data files
                if name != "DocSimilarity.py" and name !="MMR.py" and name != "TextProcessing.py" \
                   and name != "MMR_Summarizer.pyc"    and name != "DocumentScoring.py" and name != "sentence.pyc"\
                   and name != "TextProcessing.pyc"    and name != "TextProcessing.pyc" and name != "test.py" \
                   and name != "MMR_Summarizer.py"     and name != "Main.py"            and name !="sentence.py" \
                   and name != "sentence.pyc"          and name !="DocSimilarity.pyc"   and name != 'LexRankSummarizer.py'\
                   and name != 'LexRankSummarizer.pyc' and name != "DocumentScoring.pyc":
                    retval.append(os.path.join(root,name))
        return retval

    #--------------------------------------------------------------------------------------------------------
    # Method to open all documents in a given directory
    #
    # Preconditions: path is the directory for a cluster
    #
    # Returns: a list of sentence objects #please check sentence object documentation#
    #--------------------------------------------------------------------------------------------------------
    def openDirectory(self, path=None):
        # get a list of all file paths
        file_paths = self.get_all_files(path)
        
        # initialize our list of sentence objects
        sentences = []
    
        # open all files
        for file_path in file_paths:
            
            # build a list of sentence objects
            sentences = sentences + self.processFile(file_path)
            
        return sentences

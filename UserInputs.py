#=========================================================================================================
# Tafadzwa Pasipanodya
# Computer Science SYE
# Module for user interaction functionality with a summarization system
#=========================================================================================================

class UserInputs(object):
    # Standard User messages
    summarizer_options = '''
========
Options: 1. Maximum Marginal Relevance Summarization ---> 1
======== 2. LexRank Summarization                    ---> 2
'''
    option = '''Enter an option: '''

    directory_path = '''Enter a directory path: '''
    summary_length = '''Enter Summary length: '''
    query_length = '''MMR uses a query. PLease enter a query length: '''

    #------------------
    # The Constructor
    #------------------
    def __init__(self):
        pass

    #-----------------------------------------------------------------------------------------------------
    # Method to Terminate program execution once a user enters q
    #
    # Returns: void
    #-----------------------------------------------------------------------------------------------------
    def quitOnQ(self, user_input):
        if user_input == "q":
            print "Bye!"
            quit()

    #-----------------------------------------------------------------------------------------------------
    # Method to check if a user's input is a valid number
    #
    # Returns: a tuple #tuple[0] ->the integer or None if user entered an invalid integer
    #                  #tuple[1] ->the balooean value true or false base on whether user entered a real int
    #                  #    or not
    #-----------------------------------------------------------------------------------------------------
    def intIntegrityCheck(self, user_input):
        self.quitOnQ(user_input)
        n = None
        try:
            n = int(user_input)
            return n, True
        
        except ValueError:
            self.quitOnQ(n)
            print "must be an integer!"
            return (n, False)

    #-----------------------------------------------------------------------------------------------------
    # Method to prompt the user to enter an integer
    #
    # Returns: the integer when user successfuly enters one
    #-----------------------------------------------------------------------------------------------------
    def getUserInt(self, message):
        # continously prompt user for a number until correctly entered
        n, isInt = None, False
        while(isInt == False):
            n = raw_input(message)
            n, isInt = self.intIntegrityCheck(n)
        return n
        
        
    #-----------------------------------------------------------------------------------------------------
    # Method to prompt user for a directory path
    #
    # Returns: a string, the directory path
    #-----------------------------------------------------------------------------------------------------
    def getUserText(self, message):
        text = raw_input(message)
        self.quitOnQ(text)
        return text


    
    

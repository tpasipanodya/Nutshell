#===================================================================================================
# Tafadzwa Pasipanodya
# SYE
# The user interface for my summarization applications.
#===================================================================================================

import MMR_Summarizer
import LexRankSummarizer
import UserInputs

if __name__=='__main__':
    mmr = MMR_Summarizer.MMR_Summarizer()
    lexRank = LexRankSummarizer.LexRankSummarizer()
    user = UserInputs.UserInputs()
    print "Hello!\nEnter q to quit.\n"
    
    while(True):
        # get file path from user
        path = user.getUserText(user.directory_path)
        summary_length = user.getUserInt(user.summary_length)

        # get a summarizer option
        print user.summarizer_options
        summarizer_option = user.getUserInt(user.option)
        summary = []

        if summarizer_option == 1:
            query_length = user.getUserInt(user.query_length)
            summary = mmr.main(query_length, summary_length, path)

        elif summarizer_option ==2:
            summary = lexRank.main(summary_length, path)
        else:
            print "Invalid option!"

        for sent in summary:
            print "\n", sent.getOGwords(), "\n"
                




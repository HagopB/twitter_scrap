# Python 3.5
from optparse import OptionParser
from TwitterScraper import *
import os

'''***************************************************'''

#option parser
def get_comma_separated_args(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

parser = OptionParser()

parser.add_option("--scrap_type", 
                  dest="scrap_type",
                  help="Wether to stream or to slice. Only two possibilities: stream or slice")

parser.add_option("--search_query_list",
                  type='string',
                  action='callback',
                  callback=get_comma_separated_args,
                  dest="search_query_list",
                  help="The list of search queries to launch. You can run several search queries at the same time. The different queries need to be separated by a comma (',') without space. (Example: --search_query_lst arsenalfc,chelseafc,liverpool)")

parser.add_option("--max_tweets",
                  type=int,
                  dest="max_tweets",
                  help="The maximal number of tweets to consider. OPTION ONLY NECESSARY FOR THE STREAM TYPE")

parser.add_option("--tweets_since",
                  type='string',
                  dest="tweets_since",
                  help="The start date of the search. It sould be in the following form: Year-Month-Day (example: 2015-06-01)")

parser.add_option("--tweets_until",
                  type='string',
                  dest="tweets_until",
                  help="The end date of the search. It sould be in the following form: Year-Month-Day (example: 2015-07-01)")

parser.add_option("--save_path",
                  type='string',
                  dest="save_path",
                  default='./saved_tweets',
                  help="The path where to save the scrapped tweets. It will automatically creat a file in the indicated path")

parser.add_option("--print_tweets",
                  dest="print_tweets",
                  default=False,
                  help="If True all scrapped tweets will be printed.")



(options, args) = parser.parse_args()

'''***************************************************'''

if not options.scrap_type:   # if scrap_type is not given
    parser.error('Error: the scrap type must be specified. Pass --scrap_type to command line')

if options.scrap_type not in ['stream', 'slice']: # if wrong mode given
    parser.error('Error: the scrap type should be one of these choices: stream or slice. Pass --scrap_type to command line')

if not options.search_query_list: # if search_query_list is not given
    parser.error('Error: the search query list must be specified. Pass --search_query_list to command line')

if options.scrap_type == 'stream':  
    if not options.max_tweets: # if max_tweets is not given
        parser.error('Error: the maximal number of tweets must be specified. Pass --max_tweets to command line')

if options.scrap_type == 'slice':
    if not options.tweets_since: # if tweets_since is not given
        parser.error('Error: the start date of tweets scraping must be specified. Pass --tweets_since to command line')
    
    if not options.tweets_until: # if tweets_until is not given
        parser.error('Error: the end date tweets scraping must be specified. Pass --tweets_until to command line')


'''***************************************************'''
import socks
import socket

socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
socket.socket = socks.socksocket

'''***************************************************'''
print('Indicated scrap type: {}'.format(options.scrap_type))
print('Scraping for keywords: {}'.format(options.search_query_list))

if options.scrap_type == 'stream':  
    print('Max number of tweets to save in streaming: {}'.format(options.max_tweets))
else:
    print('Getting tweets between {} and {}'.format(options.tweets_since, options.tweets_until))
    
# managing the save path
if os.path.exists(options.save_path) == False:
    os.mkdir(options.save_path)
    SAVE_PATH = options.save_path
else:
    SAVE_PATH = options.save_path
    
print('Dir where tweets are saved: {}'.format(SAVE_PATH))

'''***************************************************'''
'''***************************************************'''
'''***************************************************'''

log.basicConfig(level=log.INFO)
rate_delay_seconds = 2
error_delay_seconds = 5

if options.scrap_type == 'stream':
    
    for search_query in options.search_query_list:
        
        full_path = os.path.join(SAVE_PATH, 'tweets_for_{}.pkl'.format(search_query))
        
        twit = TwitterSearchImpl(rate_delay_seconds, error_delay_seconds, options.max_tweets, full_path, options.print_tweets)
        twit.search(search_query)
        print("TwitterSearch collected %i" % twit.counter)
    
else:
    select_tweets_since = datetime.datetime.strptime(options.tweets_since, '%Y-%m-%d')
    select_tweets_until = datetime.datetime.strptime(options.tweets_until, '%Y-%m-%d')
    threads = 100
    for search_query in options.search_query_list:
        
        print('searching for {}'.format(search_query))
        full_path = os.path.join(SAVE_PATH, 'tweets_for_{}.pkl'.format(search_query))

        twitSlice = TwitterSlicer(rate_delay_seconds, error_delay_seconds, select_tweets_since, select_tweets_until,
                                  threads, full_path, options.print_tweets)
        twitSlice.search(search_query)

        print("TwitterSlicer collected %i" % twitSlice.counter)


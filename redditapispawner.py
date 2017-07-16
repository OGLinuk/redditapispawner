'''
Reddit API Bot Spawner, github.com/OGLinuk, 7/2/2017, v0.1
'''

import praw
import time
import os

def authenticate(prPrawini):
    print('Authenticating...')
    reddit = praw.Reddit('%s' % (prPrawini), user_agent='Reddit crawler')
    print('Authentication successful as %s' % (reddit.user.me()))
    return reddit

def spawn_bot(prReddit, prAcquisition_list, prSubreddit, prPayload_file, prSearchChoice):
    open('%s.txt' % (prPayload_file), 'w', encoding='UTF-8', errors='ignore')
    # Submissions
    if (prSearchChoice == 0):
        specific_search = input('Search keyword: ')
        for submission in prReddit.subreddit('%s' % (prSubreddit)).submissions():
            if specific_search in submission.title or submission.selftext and submission.id not in prAcquisition_list:
                with open('%s.txt' % (prPayload_file), 'a', encoding='UTF-8', errors='ignore') as payloadOUT:
                    print('%s \n %s' % (submission.title, submission.selftext))
                    payloadOUT.write('%s \n %s' % (submission.title, submission.selftext))
                    prAcquisition_list.append(submission.id)
                    with open('acquisition_list.txt', 'a') as acquisitionListOUT:
                        acquisitionListOUT.write('%s \n' % (submission.id))
            print('\nTaking a small break...')
            time.sleep(3)
    # Comments
    elif (prSearchChoice == 1):
        specific_search = input('Search keyword: ')
        search_limit = input('Enter a limit: ')
        for comment in prReddit.subreddit('%s' % (prSubreddit)).comments(limit=search_limit):
            if specific_search in comment.body and comment.id not in prAcquisition_list:
                with open('%s.txt' % (prPayload_file), 'a', encoding='UTF-8', errors='ignore') as payloadOUT:
                    print('%s' % (comment.body))
                    payloadOUT.write('%s' % (comment.body))
                    prAcquisition_list.append(comment.id)
                    with open('%s.txt' % (prPayload_file), 'a') as acquisitionListOUT:
                        acquisitionListOUT.write('%s \n' % (comment.id))
            print('Taking a small break...')
            time.sleep(3)

# List to prevent duplicate searches
def get_acquisition_list():
    if not os.path.isfile('acquisition_list.txt'):
        print('DID NOT FIND THE ACQUISITION LIST...')
        print('CREATING AN ACQUISITION LIST NOW...')
        open('acquisition_list.txt', 'w')
        acquisition_list = []
    else:
        with open('acquisition_list.txt', 'r') as payloadIN:
            acquisition_list = payloadIN.read()
            acquisition_list = acquisition_list.split('\n')
    return acquisition_list

def main():
    os.system('cls')
    print('----------Reddit API Bot Spawner----------\n')
    _prawini = input('Enter the name of your praw.ini file: ')
    _reddit = authenticate(_prawini)
    _acquisitionList = get_acquisition_list()
    _subreddit = input('subreddit name: ')
    _payloadFile = input('Payload filename: ')
    _searchChoice = int(input('\nPress 0 to search submissions\n\nPress 1 to search comments\n\n'))
    while True:
        spawn_bot(_reddit, _acquisitionList, _subreddit, _payloadFile, _searchChoice)

if __name__ == '__main__':
    main()

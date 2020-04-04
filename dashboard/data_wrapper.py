import numpy
import matplotlib.pyplot as plt
import timeit
import pandas as pd
import datetime, calendar
#from util import *
import ast
from textblob import *

data_path = '/Applications/MAMP/htdocs/moodle/mod/teams/dashboard/data/freecodechat/freecodecamp_casual_chatroom.csv'



def solve_mentions(x):
    for i, ms in enumerate(x):
        ous = []
        mtsasts = ast.literal_eval(ms)
        mtsast = [x for x in mtsasts]
        if len(mtsast) > 0:
            for l in mtsast:
                ou = l['screenName']
                ous.append(ou)
        mu.append(ous)


def message_polarity(content:str):
    return TextBlob(content).sentiment.polarity

def message_subjectivity(content:str):
    return TextBlob(content).sentiment.subjectivity

def cast_str(content):
    return str(content)

class DataWrapper():
    def __init__(self, path=data_path, nrows=5000):
        self.path = path
        self.data = pd.read_csv(self.path)
        self.preprocess()

    def preprocess(self):
        self.data = self.data.loc[self.data['fromUser.username']!='camperbot',:]
        self.data = self.data.loc[(~self.data['fromUser.username'].isnull()),:]
        self.data = self.data.loc[self.data['fromUser.username']!='camperbot',:]
        self.data = self.data.loc[(~self.data['fromUser.username'].isnull()),:]
        self.data = self.data.drop_duplicates()
        self.data = self.data.loc[~self.data.sent.duplicated()]
        self.data['parsed_sent'] = self.data['sent'].apply(lambda x: x[:7])
        # mu = []
        # self.data[['mentions']].apply(solve_mentions)
        # self.data['mentions.screennames'] = mu

    def get_mentions_head(self):
        return self.data['mentions.screennames'].head()


    def get_user_sent_msg_count(self, username='QuincyLarson', time_frame=None):
        """
        Function to get the messages of one user within a time frame
        Arguments: 
          - username: name of the user used to filter the messages df
          - timeframe: 
        Return:
          - user_sent:
        """

        user_sent = self.data.loc[self.data['fromUser.username']==username,
        ['fromUser.username','parsed_sent']].groupby('parsed_sent').count().reset_index()
        user_sent.rename(columns={'fromUser.username':'msgOut'}, inplace = True)
        user_sent['parsed_sent'] = pd.to_datetime(user_sent['parsed_sent'])
        user_sent.rename(columns = {'parsed_sent':'Date', 'msgOut':'Message Count'}, inplace=True)
        return user_sent

    def get_total_msg_count(self, time_frame=None):
        """
        Function to get the messages of one user within a time frame
        Arguments: 
          - username: name of the user used to filter the messages df
          - timeframe: 
        Return:
          - user_sent:

        """

        total_sent = self.data[['fromUser.username','parsed_sent']].groupby('parsed_sent').count().reset_index()
        total_sent.rename(columns={'fromUser.username':'msgOut'}, inplace = True)
        total_sent['parsed_sent'] = pd.to_datetime(total_sent['parsed_sent'])
        total_sent.rename(columns = {'parsed_sent':'Date', 'msgOut':'Message Count'}, inplace=True)
        return total_sent

    
    
    def get_user_message_content(self, username='QuincyLarson', timeframe=None):
        msgs = self.data.loc[self.data['fromUser.username']==username,['fromUser.username', 'text', 'parsed_sent']]
        #TODO: add timeframe filering
        msg_list = msgs['text'].to_list()
        return [str(i) for i in msg_list]
    
    
    def get_total_message_content(self, timeframe=None):
        msg_list = self.data['text'].to_list()
        return [str(i) for i in msg_list]
        

    def get_most_active_df(self, team=None, timeframe=None):
        most_active = self.data['fromUser.displayName'].value_counts().head(10).reset_index()
        most_active.rename(columns = {'index':'Name', 'fromUser.displayName':'Message Count'}, inplace=True)
        # usernames = most_active.keys().tolist()
        # msg_count = most_active.tolist()
        # return usernames, msg_count
        return most_active


    
    def get_least_active_df(self, team=None, timeframe=None):
        least_active = self.data['fromUser.displayName'].value_counts().tail(10).reset_index()
        least_active.rename(columns = {'index':'Name', 'fromUser.displayName':'Message Count'}, inplace=True)
        # usernames = least_active.keys().tolist()
        # msg_count = least_active.tolist()
        # return usernames, msg_count
        return least_active


    def get_sentiment_df(self, username='QuincyLarson'):
        df = self.data.loc[self.data['fromUser.username']==username,['fromUser.username', 'text', 'sent']].sort_values(by=['sent']).reset_index()
        df['text'] = df['text'].apply(cast_str)
        df['polarity'] = df['text'].apply(message_polarity)
        df['subjectivity'] = df['text'].apply(message_subjectivity)
        return df

   
    def get_team_connectivity_graph(self):
        pass

    def get_user_connectivity_graph(self):
        pass


    def get_people_related_to_user(self, username='QuincyLarson', timeframe=None):
        pass
        

    
if __name__ == "__main__":
    df = DfWrapper()
    df.preprocess()
    res = df.get_mentions_head()
    print(res)
#pip install pytrends

from pytrends.request import TrendReq
import time, os, traceback
import pandas as pd

#Most influential datapoint from item_list. Should then be removed or commented out of list
primary_key = ''
#Start - end dates in YYYY-MM-DD format. Example spanning year 2023 given
timeframe = '2023-01-01 2023-12-31'
#Leave string empty to default to web searches
gproperty = 'news'
#Refer to README for info on specifying region and category
region = ''
category = 0
#List of datapoints. Primary key is commented out
item_list = []




#File to write to, in csv format by default
trend_file = open(os.path.join(os.path.dirname(__file__), 'trendy.csv'), 'w', encoding='utf-8')

#print(len(item_list))
#Remainder searches
iterator = len(item_list) % 4
if iterator == 0: iterator = iterator + 4
if iterator != 0:
    try:

        remainder_trends = TrendReq(hl='en-US', tz=360, timeout=None)
        remainder_trends.build_payload([primary_key] + item_list[0:iterator], cat=category, timeframe=timeframe, geo=region, gprop=gproperty)

        remainder_result = remainder_trends.interest_over_time().drop('isPartial', axis=1)

        trend_file.write(remainder_result.to_csv())
        trend_file.close()

        print(remainder_result)
    except Exception:
        traceback.print_exc()

while iterator <= len(item_list):
    try:
        #Will read in remainder from file
        trend_file = open(os.path.join(os.path.dirname(__file__), 'trendy.csv'), 'r', encoding='utf-8')
        try:
            df = pd.DataFrame(pd.read_csv(trend_file))
        except: df = pd.DataFrame()
        trend_file.close()

        #Need to stagger http requests to avoid error 429
        time.sleep(5)
    
        #http requests for trends data. Uses counter to work down big_boy list of all countries excluding Israel, Turkey and Ukraine.
        pytrends = TrendReq(hl='en-US', tz=360, timeout=None)
        pytrends.build_payload([primary_key] + item_list[iterator:iterator+4], cat=category, timeframe=timeframe, geo=region, gprop=gproperty)
        looped_df = pd.DataFrame(pytrends.interest_over_time())

        #Converting to csv changes the index to a column. This causes issues because when df reads the csv it remains a column. This code removes any ambiguity by explicitely setting both as columns
        looped_df.reset_index(inplace=True)
        looped_df['date'] = pd.to_datetime(looped_df['date'], utc=True).dt.date
        df['date'] = pd.to_datetime(df['date'], utc=True).dt.date

        #Remove unnecessary columns
        dropped_looped = looped_df.drop([primary_key, 'isPartial', 'date'], axis=1)
        print(dropped_looped)

        #Merge dataframes, assign to df
        df = df.join(dropped_looped, how='outer', )
        if isinstance(df.index, pd.MultiIndex):
            df.reset_index(inplace=True)
    
        #Write new df to file, to be read in next loop until end
        trend_file = open(os.path.join(os.path.dirname(__file__), 'trendy.csv'), 'w', encoding='utf-8')
        trend_file.write(df.to_csv(index=False))
        trend_file.close()
    
        iterator = iterator + 4
    
    except Exception:
        traceback.print_exc()

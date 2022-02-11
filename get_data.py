import numpy as np
import yfinance as yf
import pandas as pd


from textblob import TextBlob
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


@st.experimental_singleton
def event_to_path(event):
    return '{}.xls'.format(event)


# data frame with manual indicators
@st.experimental_singleton
def get_self_made_data_frame(ticker,start_date,end_date):



  #download ticker data
  symbol_data_frame=yf.download(ticker,start_date,end_date)

  #add news data
  news_data_frame = pd.read_excel(event_to_path('news'), index_col = 'Date')
  symbol_data_frame=symbol_data_frame[(symbol_data_frame.index.isin(news_data_frame.index))]
  news_data_frame=news_data_frame[(news_data_frame.index.isin(symbol_data_frame.index))]

  data_frame=news_data_frame.merge(symbol_data_frame,how='inner',on=symbol_data_frame.index)
  data_frame.set_index('key_0',inplace=True)
  data_frame.index.name='Date'

  #sentiment analysis

  #clean the data
  clean_headlines=[]

  for i in data_frame['News']:
    clean_headlines.append(re.sub(r'\[\d+\]','',i)) #remove digits example:[123]


  data_frame['cleaned_news']=clean_headlines

  #create a function to get subjectivity and polarity
  def getsubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

  def getpolarity(text):
    return TextBlob(text).sentiment.polarity


  data_frame['subjectivity']=data_frame['cleaned_news'].apply(getsubjectivity)
  data_frame['polarity']=data_frame['cleaned_news'].apply(getpolarity)

  #create funtion to get sentiment scores

  def getSIA(text):
      sia=SentimentIntensityAnalyzer()
      sentiment=sia.polarity_scores(text)
      return sentiment#get the sentiment scores for each day

  compound=[]
  neg=[]
  pos=[]
  neu=[]
  SIA=0

  for i in range(0,len(data_frame['cleaned_news'])):
      SIA=getSIA(data_frame['cleaned_news'][i])
      compound.append(SIA['compound'])
      neg.append(SIA['neg'])
      neu.append(SIA['neu'])
      pos.append(SIA['pos'])


  #store the scores in merge dataset
  data_frame['compound']=compound
  data_frame['negative']=neg
  data_frame['neutral']=neu
  data_frame['positive']=pos


  data_frame=data_frame[['Open','Close','High','Low','compound','negative','neutral','positive','subjectivity','polarity']]



  return data_frame

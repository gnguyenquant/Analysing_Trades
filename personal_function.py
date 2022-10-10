from unicodedata import name
from binance import Client
#from matplotlib.pyplot import hist
from binance.enums import HistoricalKlinesType
import pandas as pd
import numpy as np

#This function is to enter the API key.
def client():
    apikey=''
    secret=''
    return Client(apikey, secret)

#This function is to take the historical data.
def historical_data(client, symbol,interval, start_date, end_date,KlinesType):
    if KlinesType=='SPOT':
        if interval=='30m':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_30MINUTE, start_date, end_date,\
            klines_type = HistoricalKlinesType.SPOT)
        elif interval=='4h':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_4HOUR, start_date, end_date,\
            klines_type = HistoricalKlinesType.SPOT)
        elif interval=='8h':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_8HOUR, start_date, end_date,\
            klines_type = HistoricalKlinesType.SPOT)
        elif interval=='12h':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_12HOUR, start_date, end_date,\
            klines_type = HistoricalKlinesType.SPOT)
        elif interval=='1d':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_date, end_date,\
            klines_type = HistoricalKlinesType.SPOT)
        elif interval=='3d':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_3DAY, start_date, end_date,\
            klines_type = HistoricalKlinesType.SPOT)
        elif interval=='1w':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1WEEK, start_date, end_date,\
            klines_type = HistoricalKlinesType.SPOT)
        else:
            return 0
        
    elif KlinesType=='FUTURES':
        if interval=='30m':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_30MINUTE, start_date, end_date,\
            klines_type = HistoricalKlinesType.FUTURES)
        elif interval=='4h':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_4HOUR,start_date, end_date,\
            klines_type = HistoricalKlinesType.FUTURES)
        elif interval=='8h':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_8HOUR,start_date, end_date,\
            klines_type = HistoricalKlinesType.FUTURES)
        elif interval=='12h':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_12HOUR,start_date, end_date,\
            klines_type = HistoricalKlinesType.FUTURES)
        elif interval=='1d':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY,start_date, end_date,\
            klines_type = HistoricalKlinesType.FUTURES)
        elif interval=='3d':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_3DAY,start_date, end_date,\
            klines_type = HistoricalKlinesType.FUTURES)
        elif interval=='1w':
            historical=client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1WEEK,start_date, end_date,\
            klines_type = HistoricalKlinesType.FUTURES)
        else:
            return 0
    else:
        return 0
    
    if len(historical)==0:
        print('the data of {} is incorrect'.format(symbol))
        return 1
    else:
        hist_df=pd.DataFrame(historical)

        hist_df.columns = ['Open Time','Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',\
                    'Quote Asset Volume', 'Number of Trades', 'TB Base Volume','TB Quote Volume','Ignore']
        hist_df['Open Time'] = pd.to_datetime(hist_df['Open Time']/1000, unit = 's')
        hist_df['Close Time'] = pd.to_datetime(hist_df['Close Time']/1000, unit = 's')
        numeric_columns=['Open', 'High', 'Low', 'Close', 'Volume',\
                        'Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']
        hist_df[numeric_columns]=hist_df[numeric_columns].apply(pd.to_numeric,axis=1)
        hist_df.drop(columns=['Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume','Close Time','Ignore','Number of Trades'], inplace=True)
        #hist_df.to_csv('{}.csv'.format(symbol))
        return hist_df

def summary(data):
    trade_history_df=pd.read_excel(data)
    trade_history_df.sort_values(by=['Market','Type'],inplace=True)
    symbols=np.array(trade_history_df['Market'])
    symbols=list(dict.fromkeys(symbols))

    summary_df=pd.DataFrame()
    summary_df['Market']=symbols
    summary_df['profit_USDT']=np.nan
    summary_df['profit_percent']=np.nan
    summary_df['remaining_amount']=np.nan

    trade_history_df.drop(columns='Fee Coin', inplace=True)

    for symbol in symbols:
        sell=trade_history_df['Total'].loc[trade_history_df['Market']==symbol]\
            .loc[trade_history_df['Type']=='SELL'].sum()
        buy=trade_history_df['Total'].loc[trade_history_df['Market']==symbol]\
            .loc[trade_history_df['Type']=='BUY'].sum()

        summary_df['profit_USDT'].loc[summary_df['Market']==symbol]=sell-buy

        summary_df['profit_percent'].loc[summary_df['Market']==symbol]\
        =summary_df['profit_USDT'].loc[summary_df['Market']==symbol]/sell*100

        summary_df['remaining_amount'].loc[summary_df['Market']==symbol]\
        =trade_history_df['Amount'].loc[trade_history_df['Market']==symbol]\
        .loc[trade_history_df['Type']=='BUY'].sum()\
        -trade_history_df['Amount'].loc[trade_history_df['Market']==symbol]\
        .loc[trade_history_df['Type']=='SELL'].sum()

    return trade_history_df, summary_df;







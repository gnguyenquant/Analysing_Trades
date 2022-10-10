#module load
from binance import Client
import pandas as pd
import personal_function as pf
import numpy as np
#from datetime import datetime

#variables

#functions
#def Merge(dict1, dict2):
#    res = {**dict1, **dict2}
#    return res

client=pf.client()
#info = client.get_account()
#status = client.get_account_status()
#details = client.get_asset_details()
#order_books_df=pd.DataFrame(columns=['symbol','price','executedQty','cummulativeQuoteQty','type'\
#    ,'side','stopPrice','time','updateTime','isWorking'])
symbols=['NEARUSDT','KAVAUSDT']
orders_1 = client.get_all_orders(symbol='NEARUSDT')
orders_2 = client.get_all_orders(symbol='KAVAUSDT')
orders_1_df=pd.DataFrame(orders_1)
orders_2_df=pd.DataFrame(orders_2)
order_concat_df=pd.concat([orders_1_df, orders_2_df])
print(order_concat_df)
"""

for symbol in symbols:
    orders = client.get_all_orders(symbol=symbol)
    orders_df=pd.DataFrame(orders)
    orders_df.drop(columns=['orderId','orderListId','clientOrderId','icebergQty','origQty','status',\
        'timeInForce','origQuoteOrderQty'],inplace=True)
    orders_df['time']=pd.to_datetime((orders_df['time']/1000).astype(int), unit='s')\
        +pd.Timedelta('08:00:00')
    orders_df['updateTime']=pd.to_datetime((orders_df['updateTime']/1000).astype(int), unit='s')\
        +pd.Timedelta('08:00:00')
    print(orders_df)
    order_books_df.append(orders_df)
"""

#print(order_books_df)

summary_data=pd.DataFrame(columns=['symbol','time buy','time sell','total buy (in USDT)'\
    ,'total sell (in USDT)','profit (in USDT)', 'profit (in %)'])
summary_data['symbol']=symbols

#for symbol in symbols:


#print(orders_df)
#time=orders_df['time'][0]
#print(time)
#time=datetime.fromtimestamp(int(time/1000))

#orders_df['time']=pd.to_datetime(orders_df['time']/1000, unit='s')
#orders_df['time']=(orders_df['time']/1000).astype(int)
#orders_df['time']=pd.to_datetime(orders_df['time'], unit='s')
#orders_df['time']=orders_df['time'] + pd.Timedelta('08:00:00')
#print(time)


trade_history_df=pd.read_excel('Trade_History.xlsx')
trade_history_df.sort_values(by=['Market','Type'],inplace=True)
#print(trade_history_df)
symbols=np.array(trade_history_df['Market'])
symbols=list(dict.fromkeys(symbols))

summary_df=pd.DataFrame()
summary_df['Market']=symbols
summary_df['profit_USDT']=np.nan
summary_df['profit_percent']=np.nan
summary_df['remaining_amount']=np.nan
summary_df['status']=np.nan
trade_history_df.drop(columns='Fee Coin', inplace=True)

for symbol in symbols:
    sell=trade_history_df['Total'].loc[trade_history_df['Market']==symbol]\
        .loc[trade_history_df['Type']=='SELL'].sum()
    buy=trade_history_df['Total'].loc[trade_history_df['Market']==symbol]\
        .loc[trade_history_df['Type']=='BUY'].sum()

    summary_df['profit_USDT'].loc[summary_df['Market']==symbol]=round(sell-buy,2)

    summary_df['profit_percent'].loc[summary_df['Market']==symbol]\
    =round(summary_df['profit_USDT'].loc[summary_df['Market']==symbol]/sell*100,2)

    summary_df['remaining_amount'].loc[summary_df['Market']==symbol]\
    =round(trade_history_df['Amount'].loc[trade_history_df['Market']==symbol]\
    .loc[trade_history_df['Type']=='BUY'].sum()\
    -trade_history_df['Amount'].loc[trade_history_df['Market']==symbol]\
    .loc[trade_history_df['Type']=='SELL'].sum(),2)

    if float(summary_df['remaining_amount'].loc[summary_df['Market']==symbol]\
        *trade_history_df['Price'].loc[trade_history_df['Market']==symbol]\
        .loc[trade_history_df['Type']=='SELL'].max())<5:
        summary_df['status'].loc[summary_df['Market']==symbol]='completed'
    else:
        summary_df['status'].loc[summary_df['Market']==symbol]='not_completed'

    #summary_df['status'].loc[summary_df['Market']==symbol]=float(summary_df['remaining_amount'].loc[summary_df['Market']==symbol]\
    #   *trade_history_df['Price'].loc[trade_history_df['Market']==symbol]\
    #    .loc[trade_history_df['Type']=='SELL'].max())

total_profit=float(summary_df['profit_USDT'].loc[summary_df['status']=='completed'].sum())


#print(trade_history_df.loc[trade_history_df['Market']=='ACMUSDT'].sum())
trade_history_df.to_csv('trade_history.csv')
summary_df.to_csv('summary.csv')
print(total_profit)
print('total profit/loss is {:.2f}'.format(total_profit))
print(summary_df)
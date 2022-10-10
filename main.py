#module load
from binance import Client
import pandas as pd
import personal_function as pf
import numpy as np

client=pf.client()

downloaded_data='Trade_History.xlsx'

trade_history_df=pd.read_excel(downloaded_data)
trade_history_df.sort_values(by=['Market','Type'],inplace=True)
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
    =round(summary_df['profit_USDT'].loc[summary_df['Market']==symbol]/buy*100,2)

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

total_profit=float(summary_df['profit_USDT'].loc[summary_df['status']=='completed'].sum())

trade_history_df.to_csv('trade_history.csv')
summary_df.to_csv('summary.csv')

with open('results.txt','w') as f:
    f.write('THE TRADING RESULTS')
    f.write('\n\n')
    f.write('TRADE HISTORY')
    f.write(trade_history_df.to_string())
    f.write('\n\nPROFIT/LOSS')
    f.write(summary_df.to_string())
    f.write('\n\ntotal realized profit/loss for completed trades: {:.2f}'.format(total_profit))
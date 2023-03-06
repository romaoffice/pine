import time
from datetime import datetime,timedelta
import backtrader as bt
import backtrader.indicators as btind
from ccxtbt import CCXTFeed
from Strategies.Strategy_2 import Strategy_2
import backtrader.analyzers as btanalyzers
import pandas as pd

def main():


   strategyNumber = 2
   startbalance = 100000.0
   maxbars = 15000
   percents_equity = 10

   totals = 0
   variation_list=[
      {'use_daily_filter':False,'pamrp_entry_bellow':True,'pamrp_entry_level':15,'pmarp_exit_level':75},
      {'use_daily_filter':True,'pamrp_entry_bellow':True,'pamrp_entry_level':15,'pmarp_exit_level':75},
      {'use_daily_filter':False,'pamrp_entry_bellow':False,'pamrp_entry_level':70,'bbwp_entry_level':40,'pmarp_exit_level':85},
      {'use_daily_filter':True,'pamrp_entry_bellow':False,'pamrp_entry_level':70,'bbwp_entry_level':40,'pmarp_exit_level':85},
      {'use_daily_filter':False,'pamrp_entry_bellow':True,'pamrp_entry_level':15,'bbwp_entry_level':40,'pmarp_exit_level':85},
      {'use_daily_filter':True,'pamrp_entry_bellow':True,'pamrp_entry_level':15,'bbwp_entry_level':40,'pmarp_exit_level':85}
   ]

   for symbol in ["BTC","ETH","BNB","ADA","XRP","LDO","SOL","MATIC","DOGE","SAND"]:
      for currentTF in [5,15,30,60,120,240,360]:
         variation_index = 0
         for params in variation_list:
            variation_index = variation_index + 1
            print('-----',symbol,currentTF,params)
            params["percents_equity"] = percents_equity
            cerebro = bt.Cerebro()
            cerebro.addstrategy(Strategy_2,params)
            cerebro.addanalyzer(btanalyzers.DrawDown, _name='drawdown')
            cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='trade')

            #prepare feed
            fromdate = datetime.now()-timedelta(minutes=currentTF*maxbars)
            todate = datetime.now()
            fromdate_daily = datetime.now()-timedelta(days=100)-timedelta(minutes=currentTF*maxbars)
            # Add the feed
            data1 = CCXTFeed(exchange='binance',
                                   dataname=symbol+'BUSD',
                                   timeframe=bt.TimeFrame.Minutes,
                                   fromdate=fromdate,
                                   todate=todate,
                                   compression=currentTF,
                                   ohlcv_limit=500,
                                   currency=symbol,
                                   retries=5,
                                   historical=True,
                                   config={
                                      'enableRateLimit': True,
                                      'options': {'defaultType': 'future'}})
            cerebro.adddata(data1)

            data2 = CCXTFeed(exchange='binance',
                                   dataname=symbol+'BUSD',
                                   timeframe=bt.TimeFrame.Days,
                                   fromdate=fromdate_daily,
                                   todate=todate,
                                   compression=1,
                                   ohlcv_limit=500,
                                   currency=symbol,
                                   retries=5,
                                   historical=True,
                                   config={
                                      'enableRateLimit': True,
                                      'options': {'defaultType': 'future'}})
            cerebro.adddata(data2)
            cerebro.broker.setcash(startbalance)
            thestrats = cerebro.run()
            thestrat = thestrats[0]
            dd = thestrat.analyzers.drawdown.get_analysis()
            trade = thestrat.analyzers.trade.get_analysis()

            mdd = round(dd.max.drawdown,2)
            netprofit = round(trade.pnl.net.total,2)
            profit_percent= round(trade.pnl.net.total/startbalance*100,2)
            if(trade.streak):
               win_trades = trade.won.total
               loss_trades = trade.lost.total
               winrate = 0 if (win_trades+loss_trades==0) else round(win_trades/(win_trades+loss_trades)*100,2)

               profit_average=round(trade.won.pnl.average,2)
               profit_max=round(trade.won.pnl.max,2)
               loss_average=round(-trade.lost.pnl.average,2)
               loss_max=round(-trade.lost.pnl.max,2)
               gross_profit = round(trade.won.pnl.total,2)
               gross_loss = round(-trade.lost.pnl.total,2)
               profit_factor = round(gross_profit/gross_loss,2) if(gross_loss>0) else None
               p_matrix = {
                 "totals":[totals],
                 "symbol":[symbol+'BUSDPerp'],
                 "tf":[currentTF],
                 "variation":[variation_index],
                 "netprofit": [netprofit],
                 "profit_percent(%)": [profit_percent],
                 "MDD(%)": [mdd],
                 "win trades": [win_trades],
                 "loss trades": [loss_trades],
                 "winrate": [winrate],
                 "W.Avg": [profit_average],
                 "W.Max": [profit_max],
                 "L.Avg": [loss_average],
                 "L.Max": [loss_max],
                 "GrossProfit": [gross_profit],
                 "GrossLoss": [gross_loss],
                 "ProfitFactor": [profit_factor]
               }
            newdf = pd.DataFrame(p_matrix)
            if(totals==0):
               df = newdf
            else:
               df=pd.concat([df,newdf])

            totals = totals +1
   df.to_csv('./result/out'+str(strategyNumber)+'.csv')
   print("Completed")
main()

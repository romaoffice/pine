
Please find attached.
- Script will trade with timefreame that attched.
- Script will use current open with "Timeframe for alert" params that is original script's param.
- When open dca, i did use threshold that is original script's param to check current price is bellow more than current open.
I am sorry for delay
Thank you.

The new task involves combining two indicators. The first indicator is named "Monthly/Weekly/Daily Open" (please see the attached file). The second indicator is actually the previous indicator ( "DCA long" and "DCA short").

 We need to use this indicator for DCA in case the price goes against entry and for closing deal alerts after DCA. 

 The long alerts must trigger based on the rules already built into the first indicator (threshold, etc.). For example, in long entry, anytime the price on a candle open (on, for example, a weekly time frame) rises and exits the threshold, the first indicator must trigger the long alert immediately. 
 It's important to note that it must not trigger any new long alerts. 

 In this case, if the price continues to rise, there's no problem, and we must check for actual take profit (close order). For closing the long position, anytime after a long entry, and if the price continues to rise until the NEXT open candle, 

 then: 1- If the NEXT candle turns red and 2- The position needs to be in the green by a minimum percentage (have the option to change this percentage) If these two conditions are met, then we need to send a close long alert! 

 However, if the price goes against our initial entry, in this case, we need to use DCA (second indicator) to average down and close the position on the green (similarly as you implemented in the previous script). 

 For DCA long, for example, if the price after the long entry falls below the candle open (for example, the weekly candle open), and the candle turns to red, then we need DCA to close the deal in green. 

 For DCA long, these rules must apply: 
 1- If the current candle entry turns red 
 2- The DCA threshold condition must apply from the moment the candle will be red after entry For example, if the DCA threshold for long entry is 10%, this means that when the candle turns red and the price falls by 10%, the DCA will start searching for a possible entry based on the timeframe conditions I explained below. So, if both conditions for DCA are met, then the DCA indicator starts searching on a certain timeframe to check the possible entry and send a DCA alert (and has the option to change those timeframes). For example, if our initial entry was on the weekly open candle, we must be able to select a separate timeframe, for example, a 1-hour timeframe for searching DCA alerts! 

 Close DCA alert: after DCA entry, if the condition for take profit in percent on the DCA indicator is met, then we must send a close DCA alert. The conditions for short entry are exactly the same but opposite. Please let me know if something is not clear. Also, if you want and if it is easy for you, you can also do separate scripts, i.e., one for long and one for short.
import backtrader as bt
import backtrader.indicators as btind

class BBWPInd(bt.Indicator):
    lines = ('bbwp',)

    params = (('i_bbwpLen', 13),
              ('i_bbwpLkbk', 252),
              ('i_basisType', 'SMA'),
              )

    def __init__(self):
        if(self.p.i_basisType=="EMA"):
            self._basis = btind.EMA(period=self.p.i_bbwpLen)
        if(self.p.i_basisType=="SMA"):
            self._basis = btind.SMA(period=self.p.i_bbwpLen)
        if(self.p.i_basisType=="WMA"):
            self._basis = btind.WMA(period=self.p.i_bbwpLen)
        if(self.p.i_basisType=="HMA"):
            self._basis = btind.HMA(period=self.p.i_bbwpLen)
        self._dev = btind.StdDev(period=self.p.i_bbwpLen)
        self._bbw = ( self._basis + self._dev - ( self._basis - self._dev )) / self._basis

    def next(self):
        _bbwSum = 0.0
        if len(self._bbw)<self.p.i_bbwpLkbk+1:
            _len = len(self._bbw)-1
        else:
            _len = self.p.i_bbwpLkbk
        for _i in range(1,_len+1):
            _bbwSum += ( 0 if self._bbw[-_i]>self._bbw[0] else 1 )
        
        self.lines.bbwp[0] = ( _bbwSum / _len)*100 if (len(self) >= self.p.i_bbwpLen) else None
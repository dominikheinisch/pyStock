# Add import from parent directory possible
import sys
import pandas as pd
import numpy
import matplotlib.pyplot as plt
from DataOperations import *

# Creates RSI object
def CreateRSI(prices,n = 14):
    return RSI(prices,n)

# Plots RSI object
def PlotRSI(rsi):
    rsi.Plot()

# RSI object which creates RSI data
class RSI:

        def __init__(self, prices, n=14):
            self.n     = n
            self.overBoughtLvl = 70
            self.overSellLvl   = 30
            self.hystersis     = 5
            self.rsi  = self.InitRSI(prices, self.n)
            self.buySignal   = CreateSubsetByValues(self.rsi, 0, 30)
            self.sellSignal  = CreateSubsetByValues(self.rsi, 70, 100)
            self.trendToFall = CreateSubsetByValues(self.rsi, 100-self.hystersis, 100)
            self.trendToRise = CreateSubsetByValues(self.rsi, 0, self.hystersis)
        
        # Set RSI indicator
        def InitRSI(self,prices,n):
            deltas = numpy.diff(prices)
            seed = deltas[:n+1]
            up = seed[seed>=0].sum()/n
            down = -seed[seed<0].sum()/n
            rs = up/down
            rsi = numpy.zeros_like(prices)
            rsi[:n] = 100. - 100./(1.+rs)

            for i in range(n, len(prices)):
                delta = deltas[i-1] # cause the diff is 1 shorter

                if delta>0:
                    upval = delta
                    downval = 0.
                else:
                    upval = 0.
                    downval = -delta

                up = (up*(n-1) + upval)/n
                down = (down*(n-1) + downval)/n

                rs = up/down
                rsi[i] = 100. - 100./(1.+rs)

            return pd.DataFrame(data=rsi,index=prices.index)

        # Plot method
        def Plot(self):
            plt.plot(self.rsi.index, self.rsi, label='RSI', color = '#000000')
            #OverBought
            overBought = CreateDataLine(self.rsi.index, 70, 70)
            plt.plot(overBought.index, overBought, '--', label='Overbought', color = '#AAAAAA')
            #OverSold
            overSold = CreateDataLine(self.rsi.index, 30, 30)
            plt.plot(overSold.index, overSold, '--', label='Oversold', color = '#AAAAAA')
            # Buy
            if (self.buySignal.size):
                plt.plot(self.buySignal.index, self.buySignal, 'x', label='Buy', color = '#00FF00')
            # Sell
            if (self.sellSignal.size):
                plt.plot(self.sellSignal.index, self.sellSignal, '*', label='Sell', color = '#FF0000')
            # Trend to Fall
            if (self.trendToFall.size):
                plt.plot(self.trendToFall.index, self.trendToFall, '*', label='ToFall', color = '#FFFF00')
            # Trend to Rise
            if (self.trendToRise.size):
                plt.plot(self.trendToRise.index, self.trendToRise, '*', label='ToRise', color = '#00FFFF')
            plt.ylim(top=100,bottom=0)

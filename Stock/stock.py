import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly_express as px
import seaborn as sns
import pandas_datareader as web
from datetime import datetime as dt
import yfinance as yf
import time


msft = yf.Ticker("MSFT")  

# get historical market data
df = msft.history(period="max")

df.dropna(inplace=True)

plt.plot(df.index, df["Close"])
plt.show()

time.sleep(10)

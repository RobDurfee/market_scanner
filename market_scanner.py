import yfinance as yf
import pandas as pd 
import pandas_helper_calc
import csv  
import datetime 
from datetime import date


"""
		        tick1	tick2	tick3	...

Current_close

ema_20
ema_50
ema_100
ema_200

d_ema_20
d_ema_50
d_ema_100
d_ema_200

score1

"""



def pull_price_history(tickers_list, start_date, end_date):
    for ticker in tickers_list:
        ticker_object = yf.Ticker(ticker)
        temp_data = ticker_object.history(start=start_date, end=end_date, interval="1d")
        output_header = ["Close"]
        temp_data.to_csv(r'ticker_data_bank\%s.csv' %ticker, columns = output_header, index = True)
    return 

def get_date_range(date_spread):
        today = date.today()
        date_delta = datetime.timedelta(days = date_spread)
        start_date = today - date_delta
        today_date_formatted = today.strftime("%Y-%m-%d")
        start_date_formatted = start_date.strftime("%Y-%m-%d")
        return today_date_formatted, start_date_formatted


def calc_indicator_EMAs(tickers_list):
    for ticker in tickers_list:
        df_temp = pd.read_csv(r"ticker_data_bank/%s.csv" %ticker)
        df_temp["EMA_10"] = df_temp["Close"].ewm(span=10, adjust=False).mean()
        #df_temp["EMA_20"] = df_temp["Close"].ewm(span=20, adjust=False).mean()
        #df_temp["EMA_50"] = df_temp["Close"].ewm(span=50, adjust=False).mean()
        #df_temp["EMA_100"] = df_temp["Close"].ewm(span=100, adjust=False).mean()
        #df_temp["EMA_200"] = df_temp["Close"].ewm(span=200, adjust=False).mean()
        df_temp.to_csv(r'ticker_data_bank\%s.csv' %ticker, index = False)
   
    return 

def indicator_derivative(tickers_list):
    for ticker in tickers_list:
        df_temp = pd.read_csv(r"ticker_data_bank/%s.csv" %ticker)
        df_temp["d_EMA_10"] = df_temp["EMA_10"].calc.derivative()

        df_temp.to_csv(r'ticker_data_bank\%s.csv' %ticker, index = False)
    return


def main():
    key_dataframe = pd.DataFrame()

    column_names = ["Ticker"]
    ticker_df = pd.read_csv('tickers_to_scan.csv', names=column_names)
    tickers_list = ticker_df.Ticker.to_list()
    today_date, start_date = get_date_range(10) #change to 365 to get full range
    
    ticker_history_data = pull_price_history(tickers_list, start_date, today_date)
    
    calc_indicator_EMAs(tickers_list)
    indicator_derivative(tickers_list)
    
    return


if __name__ == "__main__":
    main()


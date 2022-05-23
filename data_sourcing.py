# Sourcing the data for all the stocks of S&P500
# Load libraries
import pandas as pd
import bs4 as bs
import datetime as dt
import os
import pandas_datareader.data as web
import pickle
import requests
import csv
# Yahoo for dataReader
import yfinance as yf
yf.pdr_override()

import warnings
warnings.filterwarnings('ignore')

# Load dataset
# Scraping wikipedia to fetch S&P 500 stock list

def save_sp500_tickers():
    snp500url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    request_snp500 = requests.get(snp500url)
    soup = bs.BeautifulSoup(request_snp500.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable'})
    header = table.findAll("th")
    if header[0].text.rstrip() != "Symbol" or header[1].string != "Security":
        raise Exception("Can't parse Wikipedia's table!")
        # Retrieve the values in the table
    tickers = []
    rows = table.findAll("tr")
    for row in rows:
        fields = row.findAll("td")
        if fields:
            ticker = fields[0].text.rstrip()
            # fix as now they have links to the companies on WP
            #tickers.append(str(ticker) + "\n")
            tickers.append(str(ticker))
    #writer = csv.writer(open("./data/tickers_s_and_p_500.csv", "w"), lineterminator="\n")
    #writer.writerow(header)
    print('Tickers \n',tickers)
    #with open("./data/constituents_tickers.txt", "w") as f:
        # Sorting ensure easy tracking of modifications
        #tickers.sort(key=lambda s: s[0].lower())
        #f.writelines(tickers)
    return tickers


save_sp500_tickers()


def get_data_from_yahoo(reload_sp500=False):
    tickers = save_sp500_tickers()
    start = dt.datetime(2020, 1, 1)
    end = dt.datetime.now()
    dataset = yf.download(tickers, start=start, end=end)['Adj Close']
    dataset.to_csv("SP500Data.csv")
    return dataset.to_csv("SP500Data.csv")


get_data_from_yahoo()

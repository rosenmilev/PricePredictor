import requests
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import date
import json


# def get_crypto_data(fetcher, symbol, market):
# 	data = fetcher(symbol, market)
# 	data_df = pd.DataFrame(data).T
#
#
key = '30DQX6JQOX72GQ4E'
# ts = TimeSeries(key=key, output_format='pandas')
#
# data, metadata = ts.get_daily(symbol='IBM', outputsize='full')


def save_data(name, format, data):
	if format == 'json':
		current_date = date.today()
		file_path = f'{name}_{current_date}.json'
		with open(file_path, 'w') as f:
			json.dump(data, f)
		return print(f'File saved as: {file_path}')


def retrieve_data(file_path, format):
	if format == 'json':
		with open(file_path, 'r') as f:
			retrieved_data = json.load(f)
	return retrieved_data


class AlphaVantageApi:
	def __init__(self, key):
		self.key = key

	def fetch_data(self, url):
		r = requests.get(url)
		data = r.json()
		return data

	def top_gainers_losers(self):
		url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={self.key}'

		return self.fetch_data(url)


	def news_sentiment(self, tickers, date_from, topics=None, limit=10, sort='LATEST'):

		url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&' \
			  f'&time_from={date_from}apikey={self.key}&limit={limit}%sort={sort}'
		if tickers:
			url += f'&tickers={tickers}'
		elif topics:
			url += f'&topics={topics}'
		return self.fetch_data(url)



top_worst_performers = retrieve_data('top_gainers_2024-02-28.json', 'json')
df_top_gainers = pd.DataFrame(top_worst_performers['top_gainers'])
df_top_losers = pd.DataFrame(top_worst_performers['top_losers'])
df_most_actively_traded = pd.DataFrame(top_worst_performers['most_actively_traded'])



